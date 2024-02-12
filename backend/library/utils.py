from core.models import (
    Framework,
    RequirementNode,
    RequirementNode,
    RequirementLevel,
    Library,
)
from core.models import Threat, SecurityFunction, RiskMatrix
from django.contrib import messages
from django.contrib.auth.models import Permission
from iam.models import Folder, RoleAssignment
from ciso_assistant import settings
from django.utils.translation import gettext_lazy as _

from .validators import *

import os
import yaml
import json

from typing import Union, List


def get_available_library_files():
    """
    Returns a list of available library files

    Returns:
        files: list of available library files
    """
    files = []
    path = settings.BASE_DIR / "library/libraries"
    for f in os.listdir(path):
        if (
            os.path.isfile(os.path.join(path, f))
            and f.endswith(".yaml")
            or f.endswith(".yml")
        ):
            files.append(f)
    return files


def get_available_libraries():
    """
    Returns a list of available libraries

    Returns:
        libraries: list of available libraries
    """
    files = get_available_library_files()
    path = settings.BASE_DIR / "library/libraries"
    libraries = []
    for f in files:
        with open(path / f, "r", encoding="utf-8") as file:
            libs = yaml.safe_load_all(file)
            for l in list(libs):
                if (lib := Library.objects.filter(urn=l["urn"]).first()) is not None:
                    l["id"] = lib.id
                libraries.append(l)
    return libraries


def get_library_names(libraries):
    """
    Returns a list of available library names

    Returns:
        names: list of available library names
    """
    names = []
    for l in libraries:
        names.append(l.get("name"))
    return names


def get_library(urn: str) -> dict | None:
    """
    Returns a library by urn

    Args:
        urn: urn of the library to return

    Returns:
        library: library with the given urn
    """
    libraries = get_available_libraries()
    for l in libraries:
        if l["urn"] == urn:
            return l
    return None


def get_library_items(library, type: str) -> list[dict]:
    """
    Returns a list of items of a given type from a library

    Args:
        library: library to return items from
        type: type of items to return

    Returns:
        items: list of items of the given type from the library
    """
    return library["objects"].get(type, [])


class RequirementNodeImporter:
    REQUIRED_FIELDS = {"urn"}

    def __init__(self, requirement_data: dict):
        self.requirement_data = requirement_data

    def is_valid(self) -> Union[str, None]:
        if missing_fields := self.REQUIRED_FIELDS - set(self.requirement_data.keys()):
            return "Missing the following fields : {}".format(", ".join(missing_fields))

    def import_requirement_node(self, framework_object: Framework):
        requirement_node = RequirementNode.objects.create(
            # Should i just inherit the folder from Framework or this is useless ?
            folder=Folder.get_root_folder(),
            framework=framework_object,
            urn=self.requirement_data["urn"],
            parent_urn=self.requirement_data.get("parent_urn"),
            assessable=self.requirement_data.get("assessable"),
            ref_id=self.requirement_data.get("ref_id"),
            annotation=self.requirement_data.get("annotation"),
            provider=framework_object.provider,
            order_id=self.requirement_data.get("order_id"),
            level=self.requirement_data.get("level"),
            name=self.requirement_data.get("name"),
            description=self.requirement_data.get("description"),
            maturity=self.requirement_data.get("maturity"),
            locale=framework_object.locale,
            default_locale=framework_object.default_locale,
        )
    
        for threat in self.requirement_data.get("threats", []):
            requirement_node.threats.add(Threat.objects.get(urn=threat.lower()))

        for security_function in self.requirement_data.get("security_functions", []):
            requirement_node.security_functions.add(
                SecurityFunction.objects.get(urn=security_function.lower())
            )


# The couple (URN, locale) is unique. ===> Check it in the future
class FrameworkImporter:
    REQUIRED_FIELDS = {"ref_id", "urn"}
    OBJECT_FIELDS = {"requirement_nodes", "requirements"}  # "requirement_levels"

    def __init__(self, framework_data: dict):
        self.framework_data = framework_data
        # self._requirement_levels = []
        self._requirement_nodes = []

    def init_requirement_nodes(self, requirement_nodes: List[dict]) -> Union[str, None]:
        requirement_node_importers = []
        import_errors = []
        for index, requirement_node_data in enumerate(requirement_nodes):
            requirement_node_importer = RequirementNodeImporter(requirement_node_data)
            requirement_node_importers.append(requirement_node_importer)
            if (requirement_node_error := requirement_node_importer.is_valid()) is not None:
                import_errors.append((index, requirement_node_error))

        self._requirement_nodes = requirement_node_importers

        if import_errors:
            invalid_requirement_index, invalid_requirement_error = import_errors[0]
            return "[REQUIREMENT_ERROR] {} invalid requirement node{} detected, the {}{} requirement node has the following error : {}".format(
                len(import_errors),
                "s" if len(import_errors) > 1 else "",
                invalid_requirement_index + 1,
                {1: "st", 2: "nd", 3: "rd"}.get(invalid_requirement_index, "th"),
                invalid_requirement_error,
            )

    def is_empty(self):
        return (
            sum(
                len(self.framework_data.get(object_field, []))
                for object_field in self.OBJECT_FIELDS
            )
            == 0
        )

    def init(self) -> Union[str, None]:
        if missing_fields := self.REQUIRED_FIELDS - set(self.framework_data.keys()):
            return "Missing the following fields : {}".format(", ".join(missing_fields))

        detected_object_fields = self.OBJECT_FIELDS.union(self.framework_data.keys())

        if not detected_object_fields:
            return "The data must contain at least one of the following fields : {}".format(
                ", ".join(self.OBJECT_FIELDS)
            )

        if self.is_empty():
            return "No object has been detected among the object fields : {}".format(
                ", ".join(detected_object_fields)
            )

        if "requirement_nodes" in self.framework_data:
            requirement_node_data = self.framework_data["requirement_nodes"]
            if (
                requirement_node_import_error := self.init_requirement_nodes(
                    requirement_node_data
                )
            ) is not None:
                return requirement_node_import_error

    def import_framework(self, library_object: Library):
        framework_object = Framework.objects.create(
            folder=Folder.get_root_folder(),
            library=library_object,
            urn=self.framework_data["urn"],
            ref_id=self.framework_data["ref_id"],
            name=self.framework_data.get("name"),
            description=self.framework_data.get("description"),
            provider=library_object.provider,
            locale=library_object.locale,
            default_locale=library_object.default_locale,  # Change this in the future ?
        )

        for requirement_node in self._requirement_nodes:
            requirement_node.import_requirement_node(framework_object)


class ThreatImporter:
    REQUIRED_FIELDS = {"ref_id", "urn"}

    def __init__(self, threat_data: dict):
        self.threat_data = threat_data
        self._object = None

    def is_valid(self) -> Union[str, None]:
        if missing_fields := self.REQUIRED_FIELDS - set(self.threat_data.keys()):
            return "Missing the following fields : {}".format(", ".join(missing_fields))

    def import_threat(self, library_object: Library):
        Threat.objects.create(
            library=library_object,
            urn=self.threat_data.get("urn"),
            ref_id=self.threat_data["ref_id"],
            name=self.threat_data.get("name"),
            description=self.threat_data.get("description"),
            provider=library_object.provider,
            is_published=self.threat_data.get("is_published", True),
            locale=library_object.locale,
            default_locale=library_object.default_locale,  # Change this in the future ?
        )


# The couple (URN, locale) is unique. ===> Check it in the future
class SecurityFunctionImporter:
    REQUIRED_FIELDS = {"ref_id", "urn"}
    CATEGORIES = set(_category[0] for _category in SecurityFunction.CATEGORY)

    def __init__(self, security_function_data: dict):
        self.security_function_data = security_function_data

    def is_valid(self) -> Union[str, None]:
        if missing_fields := self.REQUIRED_FIELDS - set(
            self.security_function_data.keys()
        ):
            return "Missing the following fields : {}".format(", ".join(missing_fields))

        if (category := self.security_function_data.get("category")) is not None:
            if category not in SecurityFunctionImporter.CATEGORIES:
                return "Invalid category '{}', the category must be among the following list : {}".format(
                    category, ", ".join(SecurityFunctionImporter.CATEGORIES)
                )

    def import_security_function(self, library_object: Library):
        SecurityFunction.objects.create(
            library=library_object,
            urn=self.security_function_data.get("urn"),
            ref_id=self.security_function_data["ref_id"],
            name=self.security_function_data.get("name"),
            description=self.security_function_data.get("description"),
            provider=library_object.provider,
            typical_evidence=self.security_function_data.get("typical_evidence"),
            category=self.security_function_data.get("category"),
            is_published=self.security_function_data.get("is_published", True),
            locale=library_object.locale,
            default_locale=library_object.default_locale,  # Change this in the future ?
        )


# The couple (URN, locale) is unique. ===> Check this in the future
class RiskMatrixImporter:
    REQUIRED_FIELDS = {"ref_id", "urn", "json_definition"}
    MATRIX_FIELDS = {"probability", "impact", "risk", "grid"}

    def __init__(self, risk_matrix_data):
        self.risk_matrix_data = risk_matrix_data

    @staticmethod
    def is_valid_matrix(json_definition: dict) -> Union[str, None]:
        return None  # Do not verify anything for now

    def is_valid(self) -> Union[str, None]:
        return None  # Do not verify anything for now

        # Create function to check if the "JSON definition" of the matrix is wrong or not, this function will be called within this is_valid function and return an error string is an error occured or return None or success exactly like this one.

        if missing_fields := self.REQUIRED_FIELDS - set(self.risk_matrix_data.keys()):
            return "Missing the following fields : {}".format(", ".join(missing_fields))

    def import_risk_matrix(self, library_object: Library):
        matrix_data = {
            key: value
            for key, value in self.risk_matrix_data.items()
            if key in self.MATRIX_FIELDS
        }

        RiskMatrix.objects.create(
            library=library_object,
            folder=Folder.get_root_folder(),
            name=self.risk_matrix_data.get("name"),
            description=self.risk_matrix_data.get("description"),
            urn=self.risk_matrix_data.get("urn"),
            provider=library_object.provider,
            ref_id=self.risk_matrix_data.get("ref_id"),
            json_definition=json.dumps(matrix_data),
            is_enabled=self.risk_matrix_data.get("is_enabled", True),
            locale=library_object.locale,
            default_locale=library_object.default_locale,  # Change this in the future ?
        )


class LibraryImporter:
    REQUIRED_FIELDS = {"ref_id", "urn", "locale", "objects", "version"}
    OBJECT_FIELDS = ["threats", "security_functions", "risk_matrix", "framework"]

    def __init__(self, data: dict):
        self._library_data = data
        self._framework_importer = None
        self._threats = []
        self._security_functions = []
        self._risk_matrices = []

    def init_threats(self, threats: List[dict]) -> Union[str, None]:
        threat_importers = []
        import_errors = []
        for index, threat_data in enumerate(threats):
            threat_importer = ThreatImporter(threat_data)
            threat_importers.append(threat_importer)
            if (threat_error := threat_importer.is_valid()) is not None:
                import_errors.append((index, threat_error))

        self._threats = threat_importers

        if import_errors:
            # We will have to think about error message internationalization later
            invalid_threat_index, invalid_threat_error = import_errors[0]
            return "[THREAT_ERROR] {} invalid threat{} detected, the {}{} threat has the following error : {}".format(
                len(import_errors),
                "s" if len(import_errors) > 1 else "",
                invalid_threat_index + 1,
                {1: "st", 2: "nd", 3: "rd"}.get(invalid_threat_index, "th"),
                invalid_threat_error,
            )

    def init_security_functions(
        self, security_functions: List[dict]
    ) -> Union[str, None]:
        security_functions_importers = []
        import_errors = []
        for index, security_functions_data in enumerate(security_functions):
            security_function_importer = SecurityFunctionImporter(
                security_functions_data
            )
            security_functions_importers.append(security_function_importer)
            if (
                security_function_error := security_function_importer.is_valid()
            ) is not None:
                import_errors.append((index, security_function_error))

        self._security_functions = security_functions_importers

        if import_errors:
            (
                invalid_security_function_index,
                invalid_security_function_error,
            ) = import_errors[0]
            return "[SECURITY_FUNCTION_ERROR] {} invalid security function{} detected, the {}{} security function has the following error : {}".format(
                len(import_errors),
                "s" if len(import_errors) > 1 else "",
                invalid_security_function_index + 1,
                {1: "st", 2: "nd", 3: "rd"}.get(invalid_security_function_index, "th"),
                invalid_security_function_error,
            )

    def init_risk_matrices(self, risk_matrices: List[dict]) -> Union[str, None]:
        risk_matrix_importers = []
        import_errors = []
        for index, risk_matrix_data in enumerate(risk_matrices):
            risk_matrix_importer = RiskMatrixImporter(risk_matrix_data)
            risk_matrix_importers.append(risk_matrix_importer)
            if (risk_matrix_error := risk_matrix_importer.is_valid()) is not None:
                import_errors.append((index, risk_matrix_error))

        self._risk_matrices = risk_matrix_importers

        if import_errors:
            invalid_risk_matrix_index, invalid_risk_matrix_error = import_errors[0]
            return "[RISK_MATRIX_ERROR] {} invalid matri{} detected, the {}{} risk matrix has the following error : {}".format(
                len(import_errors),
                "ces" if len(import_errors) > 1 else "x",
                invalid_risk_matrix_index + 1,
                {1: "st", 2: "nd", 3: "rd"}.get(invalid_risk_matrix_index, "th"),
                invalid_risk_matrix_error,
            )

    def init_framework(self, framework_data: dict) -> Union[str, None]:
        self._framework_importer = FrameworkImporter(framework_data)
        return self._framework_importer.init()

    def init(self) -> Union[str, None]:
        missing_fields = self.REQUIRED_FIELDS - set(self._library_data.keys())
        if missing_fields:
            return "The following fields are missing in the library: {}".format(
                ", ".join(missing_fields)
            )

        library_objects = self._library_data["objects"]

        if not any(
            object_field in library_objects for object_field in self.OBJECT_FIELDS
        ):
            return "The libary 'objects' field data must contain at least one of the following fields : {}".format(
                ", ".join(self.OBJECT_FIELDS)
            )

        if "framework" in library_objects:
            framework_data = library_objects["framework"]
            if (
                framework_import_error := self.init_framework(framework_data)
            ) is not None:
                print("framework_import_error", framework_import_error)
                return framework_import_error

        if "threats" in library_objects:
            threat_data = library_objects["threats"]
            if (threat_import_error := self.init_threats(threat_data)) is not None:
                print("threat errors", threat_import_error)
                return threat_import_error

        if "risk_matrix" in library_objects:
            risk_matrix_data = library_objects["risk_matrix"]
            if (
                risk_matrix_import_error := self.init_risk_matrices(risk_matrix_data)
            ) is not None:
                return risk_matrix_import_error

        if "security_functions" in library_objects:
            security_function_data = library_objects["security_functions"]
            if (
                security_function_import_error := self.init_security_functions(
                    security_function_data
                )
            ) is not None:
                return security_function_import_error

    def import_library(self) -> Union[str, None]:
        if (error_message := self.init()) is not None:
            return error_message
        
        if self._library_data.get("dependencies"):
            for dependency in self._library_data["dependencies"]:
                if not Library.objects.filter(urn=dependency).exists():
                    import_library_view(get_library(dependency))

        _urn = self._library_data["urn"]
        _default_locale = not Library.objects.filter(urn=_urn).exists()

        # todo: import only if new or newer version
        # if Library.objects.filter(
        #     urn=self._library_data['urn'],
        #     locale=self._library_data["locale"]
        # ).exists():
        #     return "A library with the same URN and the same locale value has already been loaded !"
        _urn = self._library_data["urn"]
        _locale = self._library_data["locale"]
        library_object, _created = Library.objects.update_or_create(
            defaults={
                "ref_id": self._library_data["ref_id"],
                "name": self._library_data.get("name"),
                "description": self._library_data.get("description", None),
                "urn": _urn,
                "locale": self._library_data["locale"],
                "default_locale": _default_locale,
                "version": self._library_data.get("version", None),
                "provider": self._library_data.get("provider", None),
                "packager": self._library_data.get("packager", None),
                "folder": Folder.get_root_folder(),  # TODO: make this configurable
            },
            urn=_urn,
            locale=_locale,
        )

        import_error_msg = None
        try:
            if self._framework_importer is not None:
                self._framework_importer.import_framework(library_object)

            for threat in self._threats:
                threat.import_threat(library_object)

            for security_function in self._security_functions:
                security_function.import_security_function(library_object)

            for risk_matrix in self._risk_matrices:
                risk_matrix.import_risk_matrix(library_object)

        except Exception as e:
            print("lib exception", e)
            library_object.delete()
            raise e


def import_library_view(library: dict) -> Union[str, None]:
    """
    Imports a library

    Parameters
    ----------
    library : dict
        A library dictionary loaded from a library YAML configuration file.

    Returns
    -------
    optional_error : Union[str,None]
        A string describing the error if the function fails and returns None on success.
    """
    library_importer = LibraryImporter(library)
    return library_importer.import_library()
