import { z, type AnyZodObject } from 'zod';

export const loginSchema = z
	.object({
		username: z
			.string({
				required_error: 'Email is required'
			})
			.email(),
		password: z.string({
			required_error: 'Password is required'
		})
	})
	.required();

export const emailSchema = z
	.object({
		email: z.string({
			required_error: 'Email is required'
		})
	})
	.required();

// Utility functions for commonly used schema structures
const nameSchema = z
	.string({
		required_error: 'Name is required'
	})
	.min(1);

const descriptionSchema = z.string().optional().nullable();

const baseNamedObject = (additionalFields: any) =>
	z.object({
		name: nameSchema,
		description: descriptionSchema,
		...additionalFields
	});

export const FolderSchema = baseNamedObject({
	parent_folder: z.string().optional()
});

export const ProjectSchema = baseNamedObject({
	folder: z.string(),
	internal_reference: z.string().optional().nullable(),
	lc_status: z.string().optional().default('in_design')
});

export const RiskMatrixSchema = baseNamedObject({
	folder: z.string(),
	json_definition: z.string(),
	is_enabled: z.boolean()
});

export const LibraryUploadSchema = z.object({
	file: z.string()
});

export const RiskRiskAssessmentSchema = baseNamedObject({
	version: z.string().optional().default('0.1'),
	project: z.string(),
	risk_matrix: z.string(),
	eta: z.string().optional().nullable(),
	due_date: z.string().optional().nullable(),
	authors: z.array(z.string()).optional(),
	reviewers: z.array(z.string()).optional()
});

export const ThreatSchema = baseNamedObject({
	folder: z.string(),
	provider: z.string().optional()
});

export const RiskScenarioSchema = baseNamedObject({
	existing_measures: z.string().optional(),
	security_measures: z.string().uuid().optional().array(),
	current_proba: z.number().optional(),
	current_impact: z.number().optional(),
	residual_proba: z.number().optional(),
	residual_impact: z.number().optional(),
	treatment: z.string().optional(),
	justification: z.string().optional().nullable(),
	risk_assessment: z.string(),
	threats: z.string().uuid().optional().array(),
	assets: z.string().uuid().optional().array()
});

export const SecurityMeasureSchema = baseNamedObject({
	category: z.string().optional(),
	status: z.string().optional(),
	evidences: z.string().optional().array().optional(),
	eta: z.string().optional().nullable(),
	expiry_date: z.string().optional().nullable(),
	link: z.string().url().optional().nullable(),
	effort: z.string().optional(),
	folder: z.string(),
	security_function: z.string().optional()
});

export const RiskAcceptanceSchema = baseNamedObject({
	folder: z.string(),
	expiry_date: z.string().optional().nullable(),
	justification: z.string().optional().nullable(),
	approver: z.string(),
	risk_scenarios: z.array(z.string())
});

export const SecurityFunctionSchema = baseNamedObject({
	provider: z.string().optional().nullable(),
	category: z.string().optional(),
	folder: z.string()
});

export const AssetSchema = baseNamedObject({
	business_value: z.string().optional(),
	type: z.string(),
	folder: z.string(),
	parent_assets: z.array(z.string()).optional()
});

export const RequirementAssessmentSchema = z.object({
	status: z.string(),
	comment: z.string().optional().nullable(),
	folder: z.string(),
	requirement: z.string(),
	evidences: z.string().uuid().optional().array(),
	compliance_assessment: z.string(),
	security_measures: z.string().uuid().optional().array()
});

export const UserEditSchema = z.object({
	email: z.string().email(),
	first_name: z.string().optional(),
	last_name: z.string().optional(),
	is_active: z.boolean().optional(),
	user_groups: z.array(z.string().uuid().optional()).optional()
});

export const UserCreateSchema = z.object({ email: z.string().email() });
export const ChangePasswordSchema = z.object({
	old_password: z.string(),
	new_password: z.string(),
	confirm_new_password: z.string()
});

export const ResetPasswordSchema = z.object({
	new_password: z.string(),
	confirm_new_password: z.string()
});

export const SetPasswordSchema = z.object({
	user: z.string(),
	new_password: z.string(),
	confirm_new_password: z.string()
});

export const ComplianceAssessmentSchema = baseNamedObject({
	version: z.string().optional().default('0.1'),
	project: z.string(),
	framework: z.string(),
	eta: z.string().optional().nullable(),
	due_date: z.string().optional().nullable(),
	authors: z.array(z.string()).optional(),
	reviewers: z.array(z.string()).optional()
});

export const EvidenceSchema = baseNamedObject({
	attachment: z.string().optional().nullable(),
	folder: z.string(),
	security_measures: z.string().optional().array().optional(),
	requirement_assessments: z.string().optional().array().optional(),
	link: z.string().optional().nullable()
});

const SCHEMA_MAP: Record<string, AnyZodObject> = {
	folders: FolderSchema,
	projects: ProjectSchema,
	'risk-matrices': RiskMatrixSchema,
	'risk-assessments': RiskRiskAssessmentSchema,
	threats: ThreatSchema,
	'risk-scenarios': RiskScenarioSchema,
	'security-measures': SecurityMeasureSchema,
	'risk-acceptances': RiskAcceptanceSchema,
	'security-functions': SecurityFunctionSchema,
	assets: AssetSchema,
	'requirement-assessments': RequirementAssessmentSchema,
	'compliance-assessments': ComplianceAssessmentSchema,
	evidences: EvidenceSchema,
	users: UserCreateSchema
};

export const modelSchema = (model: string) => {
	return SCHEMA_MAP[model] || z.object({});
};
