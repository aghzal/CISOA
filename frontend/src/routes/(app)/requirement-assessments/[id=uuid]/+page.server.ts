import { BASE_API_URL } from '$lib/utils/constants';
import { getModelInfo, urlParamModelVerboseName } from '$lib/utils/crud';
import { modelSchema } from '$lib/utils/schemas';
import { listViewFields } from '$lib/utils/table';
import type { urlModel } from '$lib/utils/types';
import { tableSourceMapper, type TableSource } from '@skeletonlabs/skeleton';
import type { Actions } from '@sveltejs/kit';
import { fail, redirect } from '@sveltejs/kit';
import { setFlash } from 'sveltekit-flash-message/server';
import { setError, superValidate } from 'sveltekit-superforms/server';
import type { PageServerLoad } from './$types';

export const load = (async ({ fetch, params }) => {
	const URLModel = 'requirement-assessments';
	const endpoint = `${BASE_API_URL}/${URLModel}/${params.id}/`;

	const res = await fetch(endpoint);
	const requirementAssessment = await res.json();

	const compliance_assessment = await fetch(
		`${BASE_API_URL}/compliance-assessments/${requirementAssessment.compliance_assessment}`
	).then((res) => res.json());
	const requirement = await fetch(
		`${BASE_API_URL}/requirement-nodes/${requirementAssessment.requirement}`
	).then((res) => res.json());
	const parentRequirementNodeEndpoint = `${BASE_API_URL}/requirement-nodes/?urn=${requirement.parent_urn}`;
	let parent = await fetch(parentRequirementNodeEndpoint)
		.then((res) => res.json())
		.then((res) => res.results[0]);
	if (!parent) {
		parent = await fetch(parentRequirementNodeEndpoint)
			.then((res) => res.json())
			.then((res) => res.results[0]);
	}

	const model = getModelInfo(URLModel);

	const objectEndpoint = `${BASE_API_URL}/${URLModel}/${params.id}/object`;
	const object = await fetch(objectEndpoint).then((res) => res.json());
	const schema = modelSchema(URLModel);
	const form = await superValidate(object, schema, { errors: true });

	const foreignKeys: Record<string, any> = {};

	if (model.foreignKeyFields) {
		for (const keyField of model.foreignKeyFields) {
			const queryParams = keyField.urlParams ? `?${keyField.urlParams}` : '';
			const url = `${BASE_API_URL}/${keyField.urlModel}/${queryParams}`;
			const response = await fetch(url);
			if (response.ok) {
				foreignKeys[keyField.field] = await response.json().then((data) => data.results);
			} else {
				console.error(`Failed to fetch data for ${keyField.field}: ${response.statusText}`);
			}
		}
	}

	model.foreignKeys = foreignKeys;

	const selectOptions: Record<string, any> = {};

	if (model.selectFields) {
		for (const selectField of model.selectFields) {
			const url = `${BASE_API_URL}/${URLModel}/${selectField.field}/`;
			const response = await fetch(url);
			if (response.ok) {
				selectOptions[selectField.field] = await response.json().then((data) =>
					Object.entries(data).map(([key, value]) => ({
						label: value,
						value: key
					}))
				);
			} else {
				console.error(`Failed to fetch data for ${selectField.field}: ${response.statusText}`);
			}
		}
	}

	model['selectOptions'] = selectOptions;

	const measureCreateSchema = modelSchema('security-measures');
	const initialData = {
		folder: requirementAssessment.folder
	};

	const measureCreateForm = await superValidate(initialData, measureCreateSchema, {
		errors: false
	});

	const measureModel = getModelInfo('security-measures');
	const measureSelectOptions: Record<string, any> = {};

	if (measureModel.selectFields) {
		for (const selectField of measureModel.selectFields) {
			const url = `${BASE_API_URL}/security-measures/${selectField.field}/`;
			const response = await fetch(url);
			if (response.ok) {
				measureSelectOptions[selectField.field] = await response.json().then((data) =>
					Object.entries(data).map(([key, value]) => ({
						label: value,
						value: key
					}))
				);
			} else {
				console.error(`Failed to fetch data for ${selectField.field}: ${response.statusText}`);
			}
		}
	}

	measureModel['selectOptions'] = measureSelectOptions;

	const tables: Record<string, any> = {};

	for (const key of ['security-measures', 'evidences'] as urlModel[]) {
		const keyEndpoint = `${BASE_API_URL}/${key}/?requirement_assessments=${params.id}`;
		const response = await fetch(keyEndpoint);
		if (response.ok) {
			const data = await response.json().then((data) => data.results);

			const bodyData = tableSourceMapper(data, listViewFields[key].body);

			const table: TableSource = {
				head: listViewFields[key].head,
				body: bodyData,
				meta: data
			};
			tables[key] = table;
		} else {
			console.error(`Failed to fetch data for ${key}: ${response.statusText}`);
		}
	}

	const measureForeignKeys: Record<string, any> = {};

	if (measureModel.foreignKeyFields) {
		for (const keyField of measureModel.foreignKeyFields) {
			const queryParams = keyField.urlParams ? `?${keyField.urlParams}` : '';
			const url = `${BASE_API_URL}/${keyField.urlModel}/${queryParams}`;
			const response = await fetch(url);
			if (response.ok) {
				measureForeignKeys[keyField.field] = await response.json().then((data) => data.results);
			} else {
				console.error(`Failed to fetch data for ${keyField.field}: ${response.statusText}`);
			}
		}
	}

	measureModel.foreignKeys = measureForeignKeys;

	const evidenceModel = getModelInfo('evidences');
	const evidenceCreateSchema = modelSchema('evidences');
	const evidenceInitialData = {
		requirement_assessments: [params.id],
		folder: requirementAssessment.folder
	};
	const evidenceCreateForm = await superValidate(evidenceInitialData, evidenceCreateSchema, {
		errors: false
	});

	const evidenceSelectOptions: Record<string, any> = {};

	if (evidenceModel.selectFields) {
		for (const selectField of evidenceModel.selectFields) {
			const url = `${BASE_API_URL}/evidences/${selectField.field}/`;
			const response = await fetch(url);
			if (response.ok) {
				evidenceSelectOptions[selectField.field] = await response.json().then((data) =>
					Object.entries(data).map(([key, value]) => ({
						label: value,
						value: key
					}))
				);
			} else {
				console.error(`Failed to fetch data for ${selectField.field}: ${response.statusText}`);
			}
		}
	}

	evidenceModel['selectOptions'] = evidenceSelectOptions;

	const evidenceForeignKeys: Record<string, any> = {};

	if (evidenceModel.foreignKeyFields) {
		for (const keyField of evidenceModel.foreignKeyFields) {
			const queryParams = keyField.urlParams ? `?${keyField.urlParams}` : '';
			const url = `${BASE_API_URL}/${keyField.urlModel}/${queryParams}`;
			const response = await fetch(url);
			if (response.ok) {
				evidenceForeignKeys[keyField.field] = await response.json().then((data) => data.results);
			} else {
				console.error(`Failed to fetch data for ${keyField.field}: ${response.statusText}`);
			}
		}
	}

	evidenceModel.foreignKeys = evidenceForeignKeys;

	return {
		URLModel,
		requirementAssessment,
		compliance_assessment,
		requirement,
		parent,
		model,
		form,
		measureCreateForm,
		measureModel,
		evidenceModel,
		evidenceCreateForm,
		tables
	};
}) satisfies PageServerLoad;

export const actions: Actions = {
	updateRequirementAssessment: async (event) => {
		const URLModel = 'requirement-assessments';
		const schema = modelSchema(URLModel);
		const endpoint = `${BASE_API_URL}/${URLModel}/${event.params.id}/`;
		const form = await superValidate(event.request, schema);

		if (!form.valid) {
			console.log(form.errors);
			return fail(400, { form: form });
		}

		const requestInitOptions: RequestInit = {
			method: 'PUT',
			body: JSON.stringify(form.data)
		};

		const res = await event.fetch(endpoint, requestInitOptions);

		if (!res.ok) {
			const response = await res.json();
			console.error('server response:', response);
			if (response.non_field_errors) {
				setError(form, 'non_field_errors', response.non_field_errors);
			}
			return fail(400, { form: form });
		}
		const object = await res.json();
		const model: string = urlParamModelVerboseName(URLModel);
		setFlash({ type: 'success', message: `${model} successfully saved` }, event);
		redirect(
			302,
			event.url.searchParams.get('next') ||
				`/compliance-assessments/${object.compliance_assessment}/`
		);
	},
	createSecurityMeasure: async (event) => {
		const URLModel = 'security-measures';
		const schema = modelSchema(URLModel);
		const endpoint = `${BASE_API_URL}/${URLModel}/`;
		const form = await superValidate(event.request, schema);

		if (!form.valid) {
			console.log(form.errors);
			return fail(400, { form: form });
		}

		const requestInitOptions: RequestInit = {
			method: 'POST',
			body: JSON.stringify(form.data)
		};

		const res = await event.fetch(endpoint, requestInitOptions);

		if (!res.ok) {
			const response = await res.json();
			console.error('server response:', response);
			if (response.non_field_errors) {
				setError(form, 'non_field_errors', response.non_field_errors);
			}
			return fail(400, { form: form });
		}

		const measure = await res.json();

		const requirementAssessmentEndpoint = `${BASE_API_URL}/requirement-assessments/${event.params.id}/`;
		const requirementAssessment = await event
			.fetch(`${requirementAssessmentEndpoint}object`)
			.then((res) => res.json());

		const measures = [...requirementAssessment.security_measures, measure.id];

		const patchRequestInitOptions: RequestInit = {
			method: 'PATCH',
			body: JSON.stringify({ security_measures: measures })
		};

		const patchRes = await event.fetch(requirementAssessmentEndpoint, patchRequestInitOptions);
		if (!patchRes.ok) {
			const response = await patchRes.json();
			console.error('server response:', response);
			if (response.non_field_errors) {
				setError(form, 'non_field_errors', response.non_field_errors);
			}
			return fail(400, { form: form });
		}

		const model: string = urlParamModelVerboseName(URLModel);
		setFlash({ type: 'success', message: `${model} successfully saved: ${form.data.name}` }, event);
		return { form };
	},
	createEvidence: async (event) => {
		const URLModel = 'evidences';
		const schema = modelSchema(URLModel);
		const endpoint = `${BASE_API_URL}/${URLModel}/`;
		const formData = await event.request.formData();
		const form = await superValidate(formData, schema);

		if (!form.valid) {
			console.error(form.errors);
			return fail(400, { form: form });
		}

		const requestInitOptions: RequestInit = {
			method: 'POST',
			body: JSON.stringify(form.data)
		};

		const res = await event.fetch(endpoint, requestInitOptions);

		if (!res.ok) {
			const response = await res.json();
			console.error('server response:', response);
			if (response.non_field_errors) {
				setError(form, 'non_field_errors', response.non_field_errors);
			}
			return fail(400, { form: form });
		}

		const evidence = await res.json();
		if (formData.has('attachment')) {
			const { attachment } = Object.fromEntries(formData) as { attachment: File };
			if (attachment.size > 0) {
				const attachmentEndpoint = `${BASE_API_URL}/evidences/${evidence.id}/upload/`;
				const attachmentRequestInitOptions: RequestInit = {
					headers: {
						'Content-Disposition': `attachment; filename=${encodeURIComponent(attachment.name)}`
					},
					method: 'POST',
					body: attachment
				};
				const attachmentRes = await event.fetch(attachmentEndpoint, attachmentRequestInitOptions);
				if (!attachmentRes.ok) {
					const response = await attachmentRes.json();
					console.error(response);
					if (response.non_field_errors) {
						setError(form, 'non_field_errors', response.non_field_errors);
					}
					return fail(400, { form });
				}
			}
		}

		const model: string = urlParamModelVerboseName(URLModel);
		setFlash({ type: 'success', message: `${model} successfully saved: ${form.data.name}` }, event);
		return { form };
	}
};
