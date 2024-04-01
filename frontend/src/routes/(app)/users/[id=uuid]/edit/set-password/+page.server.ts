import { fail, redirect, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { SetPasswordSchema } from '$lib/utils/schemas';
import { setError, superValidate } from 'sveltekit-superforms/server';
import { setFlash } from 'sveltekit-flash-message/server';
import { BASE_API_URL } from '$lib/utils/constants';
import * as m from '$paraglide/messages';

export const load: PageServerLoad = async (event) => {
	const form = await superValidate(event.request, SetPasswordSchema);

	return { form };
};

export const actions: Actions = {
	default: async (event) => {
		const form = await superValidate(event.request, SetPasswordSchema);
		if (!form.valid) {
			return fail(400, { form });
		}

		const endpoint = `${BASE_API_URL}/iam/set-password/`;

		const requestInitOptions: RequestInit = {
			method: 'POST',
			body: JSON.stringify(form.data)
		};

		const res = await event.fetch(endpoint, requestInitOptions);

		if (!res.ok) {
			const response = await res.json();
			console.error('server response:', response);
			if (response.new_password) {
				setError(form, 'new_password', response.new_password);
			}
			if (response.confirm_new_password) {
				setError(form, 'confirm_new_password', response.confirm_new_password);
			}
			return fail(res.status, { form });
		}

		setFlash({ type: 'success', message: m.passwordSuccessfullySet() }, event);
		redirect(302, 'users');
	}
};
