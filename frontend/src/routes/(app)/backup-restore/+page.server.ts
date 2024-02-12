import { BASE_API_URL } from '$lib/utils/constants';
import type { Actions } from '@sveltejs/kit';
import { fail } from 'assert';

export const actions: Actions = {
	default: async ({ request, fetch }) => {
		const formData = Object.fromEntries(await request.formData());
		if (!(formData.file as File).name || (formData.file as File).name === 'undefined') {
			return fail(400, {
				error: true,
				message: 'You must provide a file to upload'
			});
		}

		const { file } = formData as { file: File };

		const endpoint = `${BASE_API_URL}/serdes/load-backup/`;
		const response = await fetch(endpoint, {
			method: 'POST',
			body: file
		});
		const data = await response.json();
		return {
			status: response.status,
			body: data
		};
	}
};
