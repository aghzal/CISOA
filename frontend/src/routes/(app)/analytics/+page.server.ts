import { BASE_API_URL } from '$lib/utils/constants';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals, fetch, params }) => {
	const req_security_measure_status = await fetch(`${BASE_API_URL}/security-measures/per_status/`);
	const security_measure_status = await req_security_measure_status.json();

	const req_ord_security_measures = await fetch(`${BASE_API_URL}/security-measures/todo/`);
	const ord_security_measures = await req_ord_security_measures.json();

	const req_get_counters = await fetch(`${BASE_API_URL}/get_counters/`);
	const counters = await req_get_counters.json();

	const req_get_risks_count_per_level = await fetch(
		`${BASE_API_URL}/risk-scenarios/count_per_level/`
	);
	const risks_count_per_level = await req_get_risks_count_per_level.json();

	const req_get_measures_to_review = await fetch(`${BASE_API_URL}/security-measures/to_review/`);
	const measures_to_review = await req_get_measures_to_review.json();

	const req_get_acceptances_to_review = await fetch(`${BASE_API_URL}/risk-acceptances/to_review/`);
	const acceptances_to_review = await req_get_acceptances_to_review.json();

	const req_get_risk_color_ordered_list = await fetch(`${BASE_API_URL}/risk-matrices/colors/`);
	const risk_color_ordered_list = await req_get_risk_color_ordered_list.json();

	const req_get_agg_data = await fetch(`${BASE_API_URL}/agg_data/`);
	const agg_data = await req_get_agg_data.json();

	const req_risk_assessments = await fetch(`${BASE_API_URL}/risk-assessments/`);
	const risk_assessments = await req_risk_assessments.json();

	const req_viewable_measures = await fetch(`${BASE_API_URL}/security-measures/`);
	const viewable_measures = await req_viewable_measures.json();

	const req_updatable_measures = await fetch(`${BASE_API_URL}/security-measures/updatables/`);
	const updatable_measures = await req_updatable_measures.json();

	const projects = await fetch(`${BASE_API_URL}/projects/`)
		.then((res) => res.json())
		.then((projects) => {
			if (projects && Array.isArray(projects.results)) {
				// Process each project to fetch its compliance assessments
				const projectPromises = projects.results.map((project) => {
					return fetch(`${BASE_API_URL}/compliance-assessments/?project=${project.id}`)
						.then((res) => res.json())
						.then((compliance_assessments) => {
							if (compliance_assessments && Array.isArray(compliance_assessments.results)) {
								// Fetch donut data for each compliance assessment
								const donutDataPromises = compliance_assessments.results.map(
									(compliance_assessment) => {
										return fetch(
											`${BASE_API_URL}/compliance-assessments/${compliance_assessment.id}/donut_data/`
										)
											.then((res) => res.json())
											.then((donutData) => {
												compliance_assessment.donut = donutData;
												return compliance_assessment; // Return the updated compliance assessment
											});
									}
								);

								// Wait for all donut data fetches to complete, then return the updated assessments
								return Promise.all(donutDataPromises).then(() => {
									project.compliance_assessments = compliance_assessments.results; // Assign the updated assessments to the project
									return project; // Return the updated project
								});
							} else {
								throw new Error('Compliance assessments results not found or not an array');
							}
						});
				});

				// Wait for all projects to be processed
				return Promise.all(projectPromises);
			} else {
				throw new Error('Projects results not found or not an array');
			}
		})
		.catch((error) => console.error('Error:', error));

	projects.forEach((project) => {
		// Initialize an object to hold the aggregated donut data
		const aggregatedDonutData = {
			values: [],
			total: 0
		};

		// Iterate through each compliance assessment of the project
		project.compliance_assessments.forEach((compliance_assessment) => {
			// Process the donut data of each assessment
			compliance_assessment.donut.values.forEach((donutItem) => {
				// Find the corresponding item in the aggregated data
				const aggregatedItem = aggregatedDonutData.values.find(
					(item) => item.name === donutItem.name
				);

				if (aggregatedItem) {
					// If the item already exists, increment its value
					aggregatedItem.value += donutItem.value;
				} else {
					// If it's a new item, add it to the aggregated data
					aggregatedDonutData.values.push({ ...donutItem });
				}
			});
		});

		// Calculate the total sum of all values
		const totalValue = aggregatedDonutData.values.reduce((sum, item) => sum + item.value, 0);

		// Calculate and store the percentage for each item
		aggregatedDonutData.values = aggregatedDonutData.values.map((item) => ({
			...item,
			percentage: totalValue > 0 ? parseFloat((item.value / totalValue) * 100).toFixed(1) : 0
		}));

		// Assign the aggregated donut data to the project
		project.overallCompliance = aggregatedDonutData;
	});

	return {
		risks_level: risks_count_per_level.results,
		measures_to_review: measures_to_review.results,
		acceptances_to_review: acceptances_to_review.results,
		colors: risk_color_ordered_list.results,
		risk_assessments: risk_assessments.results,
		viewable_measures: viewable_measures.results,
		updatable_measures: updatable_measures.results,
		agg_data: agg_data.results,
		get_counters: counters.results,
		measures: ord_security_measures.results,
		security_measure_status: security_measure_status.results,
		projects,
		user: locals.user
	};
};
