from uuid import UUID
import pytest
from ciso_assistant.settings import BASE_DIR
from core.models import *
from library.utils import *
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from iam.models import *
from core.models import *

User = get_user_model()

SAMPLE_640x480_JPG = BASE_DIR / "app_tests" / "sample_640x480.jpg"


@pytest.fixture
def root_folder_fixture():
    Folder.objects.create(
        name="Global", content_type=Folder.ContentType.ROOT, builtin=True
    )


@pytest.fixture
def risk_matrix_fixture():
    Folder.objects.create(
        name="Global", content_type=Folder.ContentType.ROOT, builtin=True
    )
    import_library_view(
        get_library("urn:intuitem:risk:library:critical_risk_matrix_5x5")
    )


@pytest.mark.django_db
class TestEvidence:
    pytestmark = pytest.mark.django_db

    @pytest.mark.usefixtures("root_folder_fixture")
    def test_evidence_parameters(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        security_measure = SecurityMeasure.objects.create(
            name="test security measure",
            description="test security measure description",
            folder=folder,
        )
        with open(SAMPLE_640x480_JPG, "rb") as f:
            evidence = Evidence.objects.create(
                name="test evidence",
                description="test evidence description",
                attachment=SimpleUploadedFile(SAMPLE_640x480_JPG.name, f.read()),
                folder=folder,
            )
            evidence.security_measures.add(security_measure)

        assert evidence.name == "test evidence"
        assert evidence.description == "test evidence description"
        assert list(evidence.security_measures.all()) == [security_measure]
        assert evidence.attachment.name.startswith(
            SAMPLE_640x480_JPG.name.split(".")[0]
        )
        assert evidence.attachment.name.endswith(".jpg")
        assert evidence.attachment.size == 106_201

    @pytest.mark.usefixtures("root_folder_fixture")
    def test_evidence_with_no_attachment(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        security_measure = SecurityMeasure.objects.create(
            name="test security measure",
            description="test security measure description",
            folder=folder,
        )
        evidence = Evidence.objects.create(
            folder=folder,
            name="test evidence",
            description="test evidence description",
        )
        evidence.security_measures.add(security_measure)
        assert not evidence.attachment


@pytest.mark.django_db
class TestRiskAssessment:
    pytestmark = pytest.mark.django_db

    def test_risk_assessment_parameters(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.create(
            name="test risk matrix",
            description="test risk matrix description",
            json_definition="{}",
            folder=folder,
        )
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )

        assert risk_assessment.name == "test risk_assessment"
        assert risk_assessment.description == "test risk_assessment description"
        assert risk_assessment.project == Project.objects.get(name="test project")
        assert risk_assessment.risk_matrix == RiskMatrix.objects.get(
            name="test risk matrix"
        )

    def test_risk_assessment_get_scenario_count_null_when_no_scenario_inside_risk_assessment(
        self,
    ):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.create(
            name="test risk matrix",
            description="test risk matrix description",
            json_definition="{}",
            folder=folder,
        )
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )

        assert risk_assessment.get_scenario_count() == 0

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_assessment_get_scenario_count_one_when_one_scenario_inside_risk_assessment(
        self,
    ):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )

        assert risk_assessment.get_scenario_count() == 1

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_assessment_get_scenario_count_is_decremented_when_child_scenario_is_deleted(
        self,
    ):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )

        assert risk_assessment.get_scenario_count() == 1

        scenario.delete()

        assert risk_assessment.get_scenario_count() == 0

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_assessment_get_scenario_count_is_incremented_when_child_scenario_is_created(
        self,
    ):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )

        assert risk_assessment.get_scenario_count() == 0

        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )

        assert risk_assessment.get_scenario_count() == 1

    def test_risk_assessment_id_is_of_type_uuid(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.create(
            name="test risk matrix",
            description="test risk matrix description",
            json_definition="{}",
            folder=folder,
        )
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )

        assert isinstance(risk_assessment.id, UUID)

    def test_risk_assessment_is_unique_in_project(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.create(
            name="test risk matrix",
            description="test risk matrix description",
            json_definition="{}",
            folder=folder,
        )
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk assessment",
            description="test risk assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        with pytest.raises(ValidationError):
            RiskAssessment.objects.create(
                name="test risk assessment",
                description="test risk assessment description",
                project=project,
                risk_matrix=risk_matrix,
            )

    def test_risk_assessment_can_have_same_name_but_different_version(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.create(
            name="test risk matrix",
            description="test risk matrix description",
            json_definition="{}",
            folder=folder,
        )
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
            version="1",
        )
        RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
            version="2",
        )

    def test_risk_assessment_can_have_same_name_and_version_in_a_different_project(
        self,
    ):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.create(
            name="test risk matrix",
            description="test risk matrix description",
            json_definition="{}",
            folder=folder,
        )
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
            version="1",
        )

        project2 = Project.objects.create(name="test project 2", folder=folder)
        RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project2,
            risk_matrix=risk_matrix,
            version="1",
        )

    def test_risk_assessment_scope_is_risk_assessments_in_project(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.create(
            name="test risk matrix",
            description="test risk matrix description",
            json_definition="{}",
            folder=folder,
        )
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        risk_assessment2 = RiskAssessment.objects.create(
            name="test risk_assessment 2",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        risk_assessment3 = RiskAssessment.objects.create(
            name="test risk_assessment 3",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )

        project2 = Project.objects.create(name="test project 2", folder=folder)
        risk_assessment4 = RiskAssessment.objects.create(
            name="test risk_assessment 4",
            description="test risk_assessment description",
            project=project2,
            risk_matrix=risk_matrix,
        )
        risk_assessment5 = RiskAssessment.objects.create(
            name="test risk_assessment 5",
            description="test risk_assessment description",
            project=project2,
            risk_matrix=risk_matrix,
        )

        assert list(risk_assessment.get_scope()) == [
            risk_assessment,
            risk_assessment2,
            risk_assessment3,
        ]


@pytest.mark.django_db
class TestRiskScenario:
    pytestmark = pytest.mark.django_db

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_scenario_parameters(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        scenario.threats.add(threat)

        assert scenario.name == "test scenario"
        assert scenario.description == "test scenario description"
        assert scenario.risk_assessment == RiskAssessment.objects.get(
            name="test risk_assessment"
        )
        assert Threat.objects.get(name="test threat") in scenario.threats.all()

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_scenario_parent_project(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )

        assert scenario.parent_project() == Project.objects.get(name="test project")

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_scenario_is_deleted_when_risk_assessment_is_deleted(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )

        queryset = RiskScenario.objects.filter(id=scenario.id)

        assert queryset.exists()

        risk_assessment.delete()

        assert not queryset.exists()

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_scenario_is__not_deleted_when_threat_is_deleted(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        scenario.threats.add(threat)

        queryset = RiskScenario.objects.filter(id=scenario.id)

        assert queryset.exists()

        threat.delete()

        assert queryset.exists()

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_scenario_id_is_of_type_uuid(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )

        assert isinstance(scenario.id, UUID)

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_scenario_scope_is_scenarios_in_risk_assessment(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        scenario2 = RiskScenario.objects.create(
            name="test scenario 2",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        scenario3 = RiskScenario.objects.create(
            name="test scenario 3",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )

        risk_assessment2 = RiskAssessment.objects.create(
            name="test risk_assessment 2",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        scenario4 = RiskScenario.objects.create(
            name="test scenario 4",
            description="test scenario description",
            risk_assessment=risk_assessment2,
        )
        scenario5 = RiskScenario.objects.create(
            name="test scenario 5",
            description="test scenario description",
            risk_assessment=risk_assessment2,
        )

        assert list(scenario.get_scope()) == [scenario, scenario2, scenario3]

    @pytest.mark.usefixtures("risk_matrix_fixture")
    def test_risk_scenario_rid_is_deterministic(self):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        scenario2 = RiskScenario.objects.create(
            name="test scenario 2",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        scenario3 = RiskScenario.objects.create(
            name="test scenario 3",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )

        assert scenario.rid == "R.1"
        assert scenario2.rid == "R.2"
        assert scenario3.rid == "R.3"


@pytest.mark.django_db
class TestRiskMatrix:
    pytestmark = pytest.mark.django_db

    ...


@pytest.mark.django_db
class TestSecurityMeasure:
    pytestmark = pytest.mark.django_db

    def test_measure_creation(self, root_folder_fixture):
        root_folder = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        measure = SecurityMeasure.objects.create(name="Measure", folder=root_folder)
        assert measure.name == "Measure"
        assert measure.folder == root_folder

    def test_measure_creation_same_name(self, root_folder_fixture):
        root_folder = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        SecurityMeasure.objects.create(name="Measure", folder=root_folder)
        with pytest.raises(ValidationError):
            SecurityMeasure.objects.create(name="Measure", folder=root_folder)

    def test_measure_creation_same_name_different_folder(self, root_folder_fixture):
        root_folder = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        folder = Folder.objects.create(name="Parent", folder=root_folder)
        measure1 = SecurityMeasure.objects.create(name="Measure", folder=root_folder)
        measure2 = SecurityMeasure.objects.create(name="Measure", folder=folder)
        assert measure1.name == "Measure"
        assert measure2.name == "Measure"
        assert measure1.folder == root_folder
        assert measure2.folder == folder

    def test_measure_category_inherited_from_function(self, root_folder_fixture):
        root_folder = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        folder = Folder.objects.create(name="Parent", folder=root_folder)
        function = SecurityFunction.objects.create(
            name="Function", folder=root_folder, category="technical"
        )
        measure = SecurityMeasure.objects.create(
            name="Measure", folder=folder, security_function=function
        )
        assert measure.category == "technical"


@pytest.mark.django_db
class TestRiskAcceptance:
    pytestmark = pytest.mark.django_db

    def test_acceptance_creation(self, risk_matrix_fixture):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        acceptance = RiskAcceptance.objects.create(
            name="test acceptance",
            description="test acceptance description",
            folder=folder,
        )
        acceptance.risk_scenarios.add(scenario)
        acceptance.save()

        assert isinstance(acceptance.id, UUID)
        assert acceptance.name == "test acceptance"
        assert acceptance.description == "test acceptance description"
        assert acceptance.folder == folder
        assert acceptance.risk_scenarios.count() == 1
        assert acceptance.risk_scenarios.all()[0] == scenario

    def test_acceptance_creation_same_name_different_folder(self, risk_matrix_fixture):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        folder2 = Folder.objects.create(
            name="test folder 2", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        acceptance = RiskAcceptance.objects.create(
            name="test acceptance",
            description="test acceptance description",
            folder=folder,
        )
        acceptance.risk_scenarios.add(scenario)
        acceptance.save()

        acceptance2 = RiskAcceptance.objects.create(
            name="test acceptance",
            description="test acceptance description",
            folder=folder2,
        )
        acceptance2.risk_scenarios.add(scenario)
        acceptance2.save()

        assert isinstance(acceptance2.id, UUID)
        assert acceptance2.name == "test acceptance"
        assert acceptance2.description == "test acceptance description"
        assert acceptance2.folder == folder2
        assert acceptance2.risk_scenarios.count() == 1
        assert acceptance2.risk_scenarios.all()[0] == scenario

    def test_acceptance_creation_same_name_same_folder(self, risk_matrix_fixture):
        folder = Folder.objects.create(
            name="test folder", description="test folder description"
        )
        risk_matrix = RiskMatrix.objects.all()[0]
        project = Project.objects.create(name="test project", folder=folder)
        risk_assessment = RiskAssessment.objects.create(
            name="test risk_assessment",
            description="test risk_assessment description",
            project=project,
            risk_matrix=risk_matrix,
        )
        threat = Threat.objects.create(
            name="test threat", description="test threat description", folder=folder
        )
        scenario = RiskScenario.objects.create(
            name="test scenario",
            description="test scenario description",
            risk_assessment=risk_assessment,
        )
        acceptance = RiskAcceptance.objects.create(
            name="test acceptance",
            description="test acceptance description",
            folder=folder,
        )
        acceptance.risk_scenarios.add(scenario)
        acceptance.save()

        with pytest.raises(ValidationError):
            acceptance2 = RiskAcceptance.objects.create(
                name="test acceptance",
                description="test acceptance description",
                folder=folder,
            )
            acceptance2.risk_scenarios.add(scenario)
            acceptance2.save()


@pytest.mark.django_db
class TestAsset:
    pytestmark = pytest.mark.django_db

    def test_asset_creation(self, root_folder_fixture):
        root_folder = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        asset = Asset.objects.create(name="Asset", folder=root_folder)
        assert asset.name == "Asset"
        assert asset.folder == root_folder
        assert asset.type == Asset.Type.SUPPORT

    def test_asset_creation_same_name(self, root_folder_fixture):
        root_folder = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        Asset.objects.create(name="Asset", folder=root_folder)
        with pytest.raises(ValidationError):
            Asset.objects.create(name="Asset", folder=root_folder)

    def test_asset_creation_same_name_different_folder(self, root_folder_fixture):
        root_folder = Folder.objects.get(content_type=Folder.ContentType.ROOT)
        folder = Folder.objects.create(name="Parent", folder=root_folder)

        asset1 = Asset.objects.create(name="Asset", folder=root_folder)
        asset2 = Asset.objects.create(name="Asset", folder=folder)
        assert asset1.name == "Asset"
        assert asset2.name == "Asset"
        assert asset1.type == Asset.Type.SUPPORT
        assert asset2.type == Asset.Type.SUPPORT
        assert asset1.folder == root_folder
        assert asset2.folder == folder
