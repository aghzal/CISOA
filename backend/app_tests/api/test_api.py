import json
import re
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from django.urls import reverse
from rest_framework import status
from ciso_assistant.settings import EMAIL_HOST, EMAIL_HOST_RESCUE

from test_vars import *


class EndpointTestsUtils:
    """Provides utils functions for API endpoints testing"""

    def get_endpoint_url(verbose_name: str, resolved: bool = True):
        """Get the endpoint URL for the given object"""

        endpoint_varname = format_endpoint(verbose_name)
        endpoint = get_var(endpoint_varname)
        return reverse(endpoint) if resolved else endpoint

    def get_object_urn(object_name: str, resolved: bool = True):
        """Get the object URN for the given object"""

        urn_varname = format_urn(object_name)
        urn = get_var(urn_varname)
        return f"{reverse(LIBRARIES_ENDPOINT)}{urn}/" if resolved else eval(urn)


class EndpointTestsQueries:
    """Provides tests functions for API endpoints testing"""

    def get_object(
        client,
        verbose_name: str,
        object=None,
        build_params: dict = None,
        endpoint: str = None,
    ):
        """Test to get object from the API without authentication

        :param client: the client (not authenticated) to use for the test
        :param verbose_name: the verbose name of the object to test
        :param object: the object to test (optional)
        :param build_params: the parameters to build the object (optional)
        :param endpoint: the endpoint URL of the object to test (optional)
        """

        url = endpoint or EndpointTestsUtils.get_endpoint_url(verbose_name)

        # Uses the API endpoint to assert that objects are not accessible
        response = client.get(url)

        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), f"{verbose_name} are accessible without authentication"
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }, f"{verbose_name} are accessible without authentication"

        # Creates a test object from the model
        if build_params and object:
            if object.__name__ == "User":
                object.objects.create_user(
                    **build_params
                )  # a password is required in the build_params
            else:
                m2m_fields = {}
                non_m2m_fields = {}

                for field, value in build_params.items():
                    if isinstance(getattr(object, field, None), ManyToManyDescriptor):
                        m2m_fields[field] = value
                    else:
                        non_m2m_fields[field] = value

                # Create the object without many-to-many fields
                test_object = object.objects.create(**non_m2m_fields)

                # Now, set the many-to-many fields
                for field, value in m2m_fields.items():
                    getattr(test_object, field).set(value)
        # Uses the API endpoint to assert that the test object is not accessible
        response = client.get(url)

        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), f"{verbose_name} are accessible without authentication"
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }, f"{verbose_name} are accessible without authentication"

    def create_object(
        client, verbose_name: str, object, test_params: dict, endpoint: str = None
    ):
        """Test to create object with the API without authentication

        :param client: the client (not authenticated) to use for the test
        :param verbose_name: the verbose name of the object to test
        :param object: the object to test
        :param test_params: the parameters of the object to test (optional)
        :param endpoint: the endpoint URL of the object to test (optional)
        """

        url = endpoint or EndpointTestsUtils.get_endpoint_url(verbose_name)
        count = object.objects.all().count()

        # Uses the API endpoint to create an object without authentication
        response = client.post(url, test_params, format="json")

        # Asserts that the user was not created
        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), f"{verbose_name} can be created without authentication"
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }, f"{verbose_name} can be created without authentication"

        # Checks that the object was not created in the database
        assert (
            count == object.objects.all().count()
        ), f"{verbose_name} created with the API without authentication are still saved in the database"

    def update_object(
        client,
        verbose_name: str,
        object,
        build_params: dict,
        update_params: dict,
        endpoint: str = None,
    ):
        """Test to update object with the API without authentication

        :param client: the client (not authenticated) to use for the test
        :param verbose_name: the verbose name of the object to test
        :param object: the object to test
        :param build_params: the parameters of the object to test
        :param update_params: the parameters to update the object
        :param endpoint: the endpoint URL of the object to test (optional)
        """

        m2m_fields = {}
        non_m2m_fields = {}

        for field, value in build_params.items():
            if isinstance(getattr(object, field, None), ManyToManyDescriptor):
                m2m_fields[field] = value
            else:
                non_m2m_fields[field] = value

        # Create the object without many-to-many fields
        test_object = object.objects.create(**non_m2m_fields)

        # Now, set the many-to-many fields
        for field, value in m2m_fields.items():
            getattr(test_object, field).set(value)

        url = endpoint or (
            EndpointTestsUtils.get_endpoint_url(verbose_name)
            + str(test_object.id)
            + "/"
        )

        # Uses the API endpoint to update an object without authentication
        response = client.patch(url, update_params, format="json")

        # Asserts that the user was not updated
        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), f"{verbose_name} can be updated without authentication"
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }, f"{verbose_name} can be updated without authentication"

        # Checks that the object was not updated in the database
        field = list(update_params.items())[0]
        assert (
            build_params[field[0]] == getattr(test_object, field[0]) != field[1]
        ), f"{verbose_name} updated with the API without authentication are still saved in the database"

    def delete_object(
        client, verbose_name: str, object, build_params: dict = {}, endpoint: str = None
    ):
        """Test to delete object with the API without authentication

        :param client: the client (not authenticated) to use for the test
        :param verbose_name: the verbose name of the object to test
        :param object: the object to test
        :param build_params: the parameters of the object to test
        :param endpoint: the endpoint URL of the object to test (optional)
        """

        if build_params:
            # Creates a test object from the model
            m2m_fields = {}
            non_m2m_fields = {}

            for field, value in build_params.items():
                if isinstance(getattr(object, field, None), ManyToManyDescriptor):
                    m2m_fields[field] = value
                else:
                    non_m2m_fields[field] = value

            # Create the object without many-to-many fields
            test_object = object.objects.create(**non_m2m_fields)

            # Now, set the many-to-many fields
            for field, value in m2m_fields.items():
                getattr(test_object, field).set(value)
            id = str(test_object.id)
        else:
            id = str(object.objects.all()[0].id)

        url = endpoint or (EndpointTestsUtils.get_endpoint_url(verbose_name) + id + "/")

        # Uses the API endpoint to delete an object without authentication
        response = client.delete(url)

        # Asserts that the user was not deleted
        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), f"{verbose_name} can be deleted without authentication"
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }, f"{verbose_name} can be deleted without authentication"

        # Checks that the object was not deleted in the database
        assert object.objects.filter(
            id=id
        ).exists(), f"{verbose_name} deleted with the API without authentication are not saved in the database"

    def import_object(client, verbose_name: str, urn: str = None):
        """Imports object with the API without authentication

        :param client: the client (not authenticated) to use for the test
        :param verbose_name: the verbose name of the object to test
        :param urn: the endpoint URL of the object to test (optional)
        """

        url = urn or EndpointTestsUtils.get_object_urn(verbose_name)

        # Uses the API endpoint to import an object without authentication
        response = client.get(url + "import/")

        # Asserts that the object was imported successfully
        assert (
            response.status_code == status.HTTP_403_FORBIDDEN
        ), f"{verbose_name} can be imported without authentication"
        assert response.json() == {
            "detail": "Authentication credentials were not provided."
        }, f"{verbose_name} can be imported without authentication"

    class Auth:
        """Provides authenticated tests functions for API endpoints testing"""

        def get_object(
            authenticated_client,
            verbose_name: str,
            object=None,
            build_params: dict = {},
            test_params: dict = {},
            base_count: int = 0,
            endpoint: str = None,
            fails: bool = False,
            expected_status: int = status.HTTP_200_OK,
        ):
            """Test to get object from the API with authentication

            :param authenticated_client: the client (authenticated) to use for the test
            :param verbose_name: the verbose name of the object to test
            :param object: the object to test (optional)
            :param build_params: the parameters to build the object (optional)
            :param test_params: the parameters of the object to test in addition to the build params (optional)
            :param base_count: the number of objects in the database before the test (optional)
                -1 means that the number of objects is unknown
            :param endpoint: the endpoint URL of the object to test (optional)
            """

            url = endpoint or EndpointTestsUtils.get_endpoint_url(verbose_name)

            # Uses the API endpoint to assert that objects are accessible
            response = authenticated_client.get(url)

            assert (
                response.status_code == expected_status
            ), f"{verbose_name} are not accessible with authentication"
            if (
                base_count == 0
                and not (object and build_params)
                and test_params
                and not fails
            ):
                # perfom a test with an externally created object
                assert (
                    response.json()["count"] == base_count + 1
                ), f"{verbose_name} are not accessible with authentication"
            elif base_count > 0 and not fails:
                assert (
                    response.json()["count"] == base_count
                ), f"{verbose_name} are not accessible with authentication"

            # Creates a test object from the model
            if build_params and object:
                if object.__name__ == "User":
                    object.objects.create_superuser(
                        **build_params
                    )  # no password is required in the build_params
                else:
                    m2m_fields = {}
                    non_m2m_fields = {}

                    for field, value in build_params.items():
                        if isinstance(
                            getattr(object, field, None), ManyToManyDescriptor
                        ):
                            m2m_fields[field] = value
                        else:
                            non_m2m_fields[field] = value

                    # Create the object without many-to-many fields
                    test_object = object.objects.create(**non_m2m_fields)

                    # Now, set the many-to-many fields
                    for field, value in m2m_fields.items():
                        getattr(test_object, field).set(value)

                # Uses the API endpoint to assert that the test object is accessible
                response = authenticated_client.get(url)

                assert (
                    response.status_code == status.HTTP_200_OK
                ), f"{verbose_name} are not accessible with authentication"

                if not fails:
                    if base_count < 0:
                        assert (
                            len(response.json()["results"]) != 0
                        ), f"{verbose_name} are not accessible with authentication"
                    else:
                        assert (
                            response.json()["count"] == base_count + 1
                        ), f"{verbose_name} are not accessible with authentication"

            if not fails:
                for key, value in {**build_params, **test_params}.items():
                    if (
                        type(value) == dict
                        and type(response.json()["results"][-1][key]) == str
                    ):
                        assert (
                            json.loads(response.json()["results"][-1][key]) == value
                        ), f"{verbose_name} {key.replace('_', ' ')} queried from the API don't match {verbose_name.lower()} {key.replace('_', ' ')} in the database"
                    else:
                        assert (
                            response.json()["results"][-1][key] == value
                        ), f"{verbose_name} {key.replace('_', ' ')} queried from the API don't match {verbose_name.lower()} {key.replace('_', ' ')} in the database"

        def get_object_options(
            authenticated_client,
            verbose_name: str,
            option: str,
            choices: list,
            endpoint: str = None,
            fails: bool = False,
            expected_status: int = status.HTTP_200_OK,
        ):
            """Test to get object options from the API with authentication

            :param authenticated_client: the client (authenticated) to use for the test
            :param verbose_name: the verbose name of the object to test
            :param object: the object to test
            :param option: the option to test
            :param endpoint: the endpoint URL of the object to test (optional)
            """

            url = endpoint or EndpointTestsUtils.get_endpoint_url(verbose_name)

            # Uses the API endpoint to assert that the object options are accessible
            response = authenticated_client.get(url + option + "/")

            assert (
                response.status_code == expected_status
            ), f"{verbose_name} {option} choices are not accessible with authentication"

            if not fails:
                for choice in choices:
                    assert (
                        choice[0] in response.json()
                    ), f"{verbose_name} {choice} choice is not accessible from the API"
                    assert (
                        str(choice[1]) in response.json()[choice[0]]
                    ), f"{verbose_name} {choice} choice is not associated to the value {choice[1]} in the API"

        def create_object(
            authenticated_client,
            verbose_name: str,
            object,
            build_params: dict,
            test_params: dict = {},
            base_count: int = 0,
            endpoint: str | None = None,
            query_format: str = "json",
            fails: bool = False,
            expected_status: int = status.HTTP_201_CREATED,
        ):
            """Test to create object with the API with authentication

            :param authenticated_client: the client (authenticated) to use for the test
            :param verbose_name: the verbose name of the object to test
            :param build_params: the parameters to build the object
            :param test_params: the parameters of the object to test in addition to the build params (optional)
                the test_params can ovveride the build_params
            :param base_count: the number of objects in the database before the test (optional)
                -1 means that the number of objects is unknown
            :param endpoint: the endpoint URL of the object to test (optional)
            """

            url = endpoint or EndpointTestsUtils.get_endpoint_url(verbose_name)

            # Uses the API endpoint to create an object with authentication
            response = authenticated_client.post(url, build_params, format=query_format)

            # Asserts that the object was created successfully
            assert (
                response.status_code == expected_status
            ), f"{verbose_name} can not be created with authentication"

            for key, value in build_params.items():
                if key == "attachment":
                    # Asserts that the value file name is present in the JSON response
                    assert (
                        value.name.split("/")[-1].split(".")[0] in response.json()[key]
                    ), f"{verbose_name} {key.replace('_', ' ')} returned by the API after object creation don't match the provided {key.replace('_', ' ')}"
                else:
                    assert (
                        response.json()[key] == value
                    ), f"{verbose_name} {key.replace('_', ' ')} returned by the API after object creation don't match the provided {key.replace('_', ' ')}"

            # Checks that the object was created in the database
            assert (
                object.objects.filter(id=response.json()["id"]).exists()
            ), f"{verbose_name} created with the API are not saved in the database"

            # Uses the API endpoint to assert that the created object is accessible
            response = authenticated_client.get(url)

            assert (
                response.status_code == status.HTTP_200_OK
            ), f"{verbose_name} are not accessible with authentication"

            for key, value in {**build_params, **test_params}.items():
                if (
                    key == "attachment"
                    and response.json()["results"][base_count][key] != value
                ):
                    # Asserts that the value file name is present in the JSON response
                    assert (
                        re.sub(
                            r"_([a-z]|[A-Z]|[0-9]){7}(?:\.)",
                            ".",
                            response.json()["results"][base_count][key],
                        )
                        == value
                    ), f"{verbose_name} {key.replace('_', ' ')} queried from the API don't match {verbose_name.lower()} {key.replace('_', ' ')} in the database"
                else:
                    assert (
                        response.json()["results"][base_count][key] == value
                    ), f"{verbose_name} {key.replace('_', ' ')} queried from the API don't match {verbose_name.lower()} {key.replace('_', ' ')} in the database"

        def update_object(
            authenticated_client,
            verbose_name: str,
            object,
            build_params: dict,
            update_params: dict,
            test_build_params: dict = {},
            test_params: dict = {},
            endpoint: str | None = None,
            query_format: str = "json",
            fails: bool = False,
            expected_status: int = status.HTTP_200_OK,
        ):
            """Test to update object with the API with authentication

            :param authenticated_client: the client (authenticated) to use for the test
            :param verbose_name: the verbose name of the object to test
            :param build_params: the parameters to build the object
            :param update_params: the parameters to update the object
            :param test_params: the parameters of the modified object to test (optional)
                the test_params can ovveride the build_params
            :param endpoint: the endpoint URL of the object to test (optional)
            """

            # Creates a test object from the model
            m2m_fields = {}
            non_m2m_fields = {}

            for field, value in build_params.items():
                if isinstance(getattr(object, field, None), ManyToManyDescriptor):
                    m2m_fields[field] = value
                else:
                    non_m2m_fields[field] = value

            # Create the object without many-to-many fields
            test_object = object.objects.create(**non_m2m_fields)
            id = str(test_object.id)

            # Now, set the many-to-many fields
            for field, value in m2m_fields.items():
                getattr(test_object, field).set(value)

            url = endpoint or (
                EndpointTestsUtils.get_endpoint_url(verbose_name)
                + str(test_object.id)
                + "/"
            )

            response = authenticated_client.get(url)

            assert (
                response.status_code == status.HTTP_200_OK
            ), f"{verbose_name} can not be updated with authentication"
            for key, value in {**build_params, **test_build_params}.items():
                if key == "attachment":
                    # Asserts that the value file name is present in the JSON response
                    assert (
                        value.name.split("/")[-1].split(".")[0] in response.json()[key]
                    ), f"{verbose_name} {key.replace('_', ' ')} returned by the API after object creation don't match the provided {key.replace('_', ' ')}"
                else:
                    assert (
                        response.json()[key] == value
                    ), f"{verbose_name} {key.replace('_', ' ')} queried from the API don't match {verbose_name.lower()} {key.replace('_', ' ')} in the database"

            update_response = authenticated_client.patch(
                url, update_params, format=query_format
            )

            assert (
                update_response.status_code == expected_status
            ), f"{verbose_name} can not be updated with authentication"
            for key, value in {**build_params, **update_params, **test_params}.items():
                if not fails:
                    if key == "attachment" and update_response.json()[key] != value:
                        # Asserts that the value file name is present in the JSON response
                        assert (
                            value.split("/")[-1].split(".")[0]
                            in update_response.json()[key]
                        ), f"{verbose_name} {key.replace('_', ' ')} queried from the API don't match {verbose_name.lower()} {key.replace('_', ' ')} in the database"
                    else:
                        assert (
                            update_response.json()[key] == value
                        ), f"{verbose_name} {key.replace('_', ' ')} queried from the API don't match {verbose_name.lower()} {key.replace('_', ' ')} in the database"

        def delete_object(
            authenticated_client,
            verbose_name: str,
            object,
            build_params: dict = {},
            endpoint: str = None,
            fails: bool = False,
            expected_status: int = status.HTTP_204_NO_CONTENT,
        ):
            """Test to delete object with the API with authentication

            :param authenticated_client: the client (authenticated) to use for the test
            :param verbose_name: the verbose name of the object to test
            :param build_params: the parameters to build the object
            :param endpoint: the endpoint URL of the object to test (optional)
            """

            if build_params:
                # Creates a test object from the model
                m2m_fields = {}
                non_m2m_fields = {}

                for field, value in build_params.items():
                    if isinstance(getattr(object, field, None), ManyToManyDescriptor):
                        m2m_fields[field] = value
                    else:
                        non_m2m_fields[field] = value

                # Create the object without many-to-many fields
                test_object = object.objects.create(**non_m2m_fields)
                id = str(test_object.id)

                # Now, set the many-to-many fields
                for field, value in m2m_fields.items():
                    getattr(test_object, field).set(value)
            else:
                id = str(object.objects.all()[0].id)

            url = endpoint or (
                EndpointTestsUtils.get_endpoint_url(verbose_name) + id + "/"
            )

            # Asserts that the objects exists
            response = authenticated_client.get(url)
            assert (
                response.status_code == status.HTTP_200_OK
            ), f"{verbose_name} can not be deleted with authentication"

            # Asserts that the object was deleted successfully
            delete_response = authenticated_client.delete(url)
            assert (
                delete_response.status_code == expected_status
            ), f"{verbose_name} can not be deleted with authentication"

            # Asserts that the objects does not exists anymore
            response = authenticated_client.get(url)
            assert (
                response.status_code == status.HTTP_404_NOT_FOUND
            ), f"{verbose_name} has not been properly deleted with authentication"

        def import_object(
            authenticated_client,
            verbose_name: str,
            urn: str | None = None,
            fails: bool = False,
            expected_status: int = status.HTTP_200_OK,
        ):
            """Imports object with the API with authentication

            :param authenticated_client: the client (authenticated) to use for the test
            :param verbose_name: the verbose name of the object to test
            :param urn: the endpoint URL of the object to test (optional)
            """

            url = urn or EndpointTestsUtils.get_object_urn(verbose_name)

            # Uses the API endpoint to import an object with authentication
            response = authenticated_client.get(url + "import/")

            # Asserts that the object was imported successfully
            assert (
                response.status_code == expected_status
            ), f"{verbose_name} can not be imported with authentication"
            if not fails:
                assert response.json() == {
                    "status": "success"
                }, f"{verbose_name} can not be imported with authentication"

        def compare_results(
            authenticated_client,
            object_name: str,
            compare_url: str,
            reference_url: str,
            test_params: list,
            count: int = 5,
            fails: bool = False,
            expected_status: int = status.HTTP_200_OK,
        ):
            """Test to compare 2 endpoints results from the API with authentication

            :param authenticated_client: the client (authenticated) to use for the test
            :param object_name: the name of the object to compare
            :param compare_url: the endpoint URL of the endpoint to compare
            :param reference_url: the endpoint URL of the reference endpoint to compare to
            :param test_params: the parameters to test
                params can be a tuple with the parameter name and the expected value or a string with the parameter name
            :param count: the number of objects to tests for each endpoint - default is 5
            """

            # Uses the API endpoints to get the reference objects list
            reference = authenticated_client.get(reference_url)
            assert (
                reference.status_code == status.HTTP_200_OK
            ), f"reference endpoint is not accessible with authentication"

            for object in reference.json()["objects"]["framework"][
                object_name.lower().replace(" ", "_")
            ][:count]:
                comparelist = authenticated_client.get(compare_url)
                compare = None
                assert (
                    comparelist.status_code == expected_status
                ), f"{object['name']} is not in {compare_url} results"

                # find the object in the objects list
                if not fails:
                    for c in comparelist.json()["results"]:
                        if c["urn"] == object["urn"]:
                            compare = c

                # assert that the values are the same for the given parameters
                for param in test_params:
                    if param in object and param in compare:
                        if type(param) == tuple:
                            assert (
                                object[param[0]] == param[1]
                            ), f"the reference {param[0]} value is not {param[1]}"
                            assert (
                                compare[param[0]] == param[1]
                            ), f"the endpoint to compare {param[0]} value is not {param[1]}"
                        else:
                            assert (
                                compare[param] == object[param]
                            ), f"the endpoint to compare {param[0]} value is not {param[1]}"
