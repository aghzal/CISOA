from typing import Any
from ciso_assistant.settings import EMAIL_HOST, EMAIL_HOST_RESCUE

from core.models import *
from iam.models import *

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import models
from core.serializer_fields import FieldsRelatedField

User = get_user_model()


class BaseModelSerializer(serializers.ModelSerializer):
    def update(self, instance: models.Model, validated_data: Any) -> models.Model:
        if hasattr(instance, "urn") and getattr(instance, "urn"):
            raise serializers.ValidationError(
                {"urn": "Imported objects cannot be modified"}
            )
        return super().update(instance, validated_data)

    class Meta:
        model: models.Model


class AssessmentReadSerializer(BaseModelSerializer):
    project = FieldsRelatedField()
    authors = FieldsRelatedField(many=True)
    reviewers = FieldsRelatedField(many=True)


# Risk Assessment


class RiskMatrixReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()

    class Meta:
        model = RiskMatrix
        fields = "__all__"


class RiskMatrixWriteSerializer(RiskMatrixReadSerializer):
    pass


class RiskAcceptanceWriteSerializer(BaseModelSerializer):
    # NOTE: This is a workaround to filter the approvers on api view
    #       but it causes some problems in api_tests. Serializers are
    #       called before to create users, so the approvers_id list
    #       is empty and the api_tests fail.
    # approvers_id = []
    # try:
    #     for candidate in User.objects.all():
    #         if RoleAssignment.has_permission(candidate, 'approve_riskacceptance'):
    #             approvers_id.append(candidate.id)
    # except:
    #     pass
    # approver = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(id__in=approvers_id))

    class Meta:
        model = RiskAcceptance
        exclude = ["accepted_at", "rejected_at", "revoked_at", "state"]


class RiskAcceptanceReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()
    approver = FieldsRelatedField()
    risk_scenarios = FieldsRelatedField(many=True)

    state = serializers.CharField(source="get_state_display")

    class Meta:
        model = RiskAcceptance
        fields = "__all__"


class ProjectWriteSerializer(BaseModelSerializer):
    class Meta:
        model = Project
        exclude = ["created_at"]


class ProjectReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()
    lc_status = serializers.CharField(source="get_lc_status_display")

    class Meta:
        model = Project
        fields = "__all__"


class RiskAssessmentWriteSerializer(BaseModelSerializer):
    class Meta:
        model = RiskAssessment
        exclude = ["created_at", "updated_at"]


class RiskAssessmentReadSerializer(AssessmentReadSerializer):
    risk_scenarios = FieldsRelatedField(many=True)
    risk_matrix = FieldsRelatedField()

    class Meta:
        model = RiskAssessment
        fields = "__all__"


class AssetWriteSerializer(BaseModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class AssetReadSerializer(AssetWriteSerializer):
    folder = FieldsRelatedField()
    parent_assets = FieldsRelatedField(many=True)

    type = serializers.CharField(source="get_type_display")


class SecurityFunctionWriteSerializer(BaseModelSerializer):
    class Meta:
        model = SecurityFunction
        fields = "__all__"


class SecurityFunctionReadSerializer(SecurityFunctionWriteSerializer):
    folder = FieldsRelatedField()


class ThreatWriteSerializer(BaseModelSerializer):
    class Meta:
        model = Threat
        fields = "__all__"

    # ["id", "folder", "ref_id", "name", "description", "provider"] # TODO: check why not all?


class ThreatReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()

    class Meta:
        model = Threat
        fields = "__all__"


class RiskScenarioWriteSerializer(BaseModelSerializer):
    risk_matrix = serializers.PrimaryKeyRelatedField(
        read_only=True, source="risk_assessment.risk_matrix"
    )

    class Meta:
        model = RiskScenario
        fields = "__all__"


class RiskScenarioReadSerializer(RiskScenarioWriteSerializer):
    risk_assessment = FieldsRelatedField()
    risk_matrix = FieldsRelatedField(source="risk_assessment.risk_matrix")
    project = FieldsRelatedField(
        source="risk_assessment.project", fields=["id", "name", "folder"]
    )
    version = serializers.StringRelatedField(source="risk_assessment.version")
    threats = FieldsRelatedField(many=True)
    assets = FieldsRelatedField(many=True)

    treatment = serializers.CharField(source="get_treatment_display")

    current_proba = serializers.CharField(source="get_current_proba.name")
    current_impact = serializers.CharField(source="get_current_impact.name")
    current_level = serializers.JSONField(source="get_current_risk")
    residual_proba = serializers.CharField(source="get_residual_proba.name")
    residual_impact = serializers.CharField(source="get_residual_impact.name")
    residual_level = serializers.JSONField(source="get_residual_risk")

    security_measures = FieldsRelatedField(many=True)


class SecurityMeasureWriteSerializer(BaseModelSerializer):
    class Meta:
        model = SecurityMeasure
        fields = "__all__"


class SecurityMeasureReadSerializer(SecurityMeasureWriteSerializer):
    folder = FieldsRelatedField()
    security_function = FieldsRelatedField()

    category = serializers.CharField(
        source="get_category_display"
    )  # type : get_type_display
    status = serializers.CharField(source="get_status_display")
    evidences = FieldsRelatedField(many=True)
    effort = serializers.CharField(source="get_effort_display")


class UserReadSerializer(BaseModelSerializer):
    user_groups = FieldsRelatedField(many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "user_groups",
        ]


class UserWriteSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "date_joined",
            "user_groups",
        ]

    def validate_email(self, email):
        validate_email(email)
        return email

    def create(self, validated_data):
        send_mail = EMAIL_HOST or EMAIL_HOST_RESCUE
        try:
            user = User.objects.create_user(**validated_data)
        except Exception as e:
            print(e)
            if User.objects.filter(email=validated_data["email"]).exists() and send_mail:
                raise serializers.ValidationError(
                    {
                        "warning": [
                            "User created successfully but an error occurred while sending the email"
                        ]
                    }
                )
            else:
                raise serializers.ValidationError(
                    {
                        "error": [
                            "An error occurred while creating the user"
                        ]
                    }
                )
        return user


class UserGroupReadSerializer(BaseModelSerializer):
    name = serializers.CharField(source="__str__")
    label = serializers.CharField(source="get_name_display")
    folder = FieldsRelatedField()

    class Meta:
        model = UserGroup
        fields = "__all__"


class UserGroupWriteSerializer(BaseModelSerializer):
    class Meta:
        model = UserGroup
        fields = "__all__"


class RoleReadSerializer(BaseModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RoleWriteSerializer(BaseModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RoleAssignmentReadSerializer(BaseModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = "__all__"


class RoleAssignmentWriteSerializer(BaseModelSerializer):
    class Meta:
        model = RoleAssignment
        fields = "__all__"


class FolderWriteSerializer(BaseModelSerializer):
    class Meta:
        model = Folder
        exclude = [
            "builtin",
            "content_type",
        ]


class FolderReadSerializer(BaseModelSerializer):
    parent_folder = FieldsRelatedField()

    content_type = serializers.CharField(source="get_content_type_display")

    class Meta:
        model = Folder
        exclude = []


# Compliance Assessment


class FrameworkReadSerializer(BaseModelSerializer):
    folder = FieldsRelatedField()

    class Meta:
        model = Framework
        fields = "__all__"


class FrameworkWriteSerializer(FrameworkReadSerializer):
    pass


class RequirementLevelReadSerializer(BaseModelSerializer):
    class Meta:
        model = RequirementLevel
        fields = "__all__"


class RequirementLevelWriteSerializer(RequirementLevelReadSerializer):
    pass


class RequirementNodeReadSerializer(BaseModelSerializer):
    security_functions = FieldsRelatedField(many=True)
    threats = FieldsRelatedField(many=True)
    display_short = serializers.CharField()
    display_long = serializers.CharField()

    class Meta:
        model = RequirementNode
        fields = "__all__"


class RequirementNodeWriteSerializer(RequirementNodeReadSerializer):
    pass


class EvidenceReadSerializer(BaseModelSerializer):
    attachment = serializers.CharField(source="filename")
    folder = FieldsRelatedField()
    security_measures = FieldsRelatedField(many=True)
    requirement_assessments = FieldsRelatedField(many=True)

    class Meta:
        model = Evidence
        fields = "__all__"


class EvidenceWriteSerializer(BaseModelSerializer):
    security_measures = serializers.PrimaryKeyRelatedField(many=True, queryset=SecurityMeasure.objects.all())
    requirement_assessments = serializers.PrimaryKeyRelatedField(many=True, queryset=RequirementAssessment.objects.all())
    class Meta:
        model = Evidence
        fields = "__all__"


class AttachmentUploadSerializer(serializers.Serializer):
    attachment = serializers.FileField(required=True)

    class Meta:
        model = Evidence
        fields = ["attachment"]


class ComplianceAssessmentReadSerializer(AssessmentReadSerializer):
    framework = FieldsRelatedField()

    class Meta:
        model = ComplianceAssessment
        fields = "__all__"


class ComplianceAssessmentWriteSerializer(BaseModelSerializer):
    class Meta:
        model = ComplianceAssessment
        fields = "__all__"


class RequirementAssessmentReadSerializer(BaseModelSerializer):
    name = serializers.CharField(source="__str__")

    class Meta:
        model = RequirementAssessment
        fields = "__all__"


class RequirementAssessmentWriteSerializer(BaseModelSerializer):
    class Meta:
        model = RequirementAssessment
        fields = "__all__"
