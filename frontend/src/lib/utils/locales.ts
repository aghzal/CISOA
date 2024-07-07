import * as m from '../../paraglide/messages';

export const LOCALE_MAP = {
	en: {
		name: 'english',
		flag: '🇬🇧'
	},
	fr: {
		name: 'french',
		flag: '🇫🇷'
	},
	de: {
		name: 'german',
		flag: '🇩🇪'
	},
	ar: {
		name: 'arabic',
		flag: '🇸🇦'
	},
	pt: {
		name: 'portuguese',
		flag: '🇧🇷'
	},
	es: {
		name: 'spanish',
		flag: '🇪🇸'
	},
	nl: {
		name: 'dutch',
		flag: '🇳🇱'
	},
	it: {
		name: 'italian',
		flag: '🇮🇹'
	},
	pl: {
		name: 'polish',
		flag: '🇵🇱'
	}
};

export function toCamelCase(str: string) {
	if (typeof str !== 'string') return str;
	str = str.charAt(0).toLowerCase() + str.slice(1);
	return str.replace(/[_-\s]\w/g, (match) => match.charAt(1).toUpperCase());
}

export function capitalizeFirstLetter(str: string) {
	return str.charAt(0).toUpperCase() + str.slice(1);
}

interface LocalItems {
	[key: string]: string;
}

export function localItems(): LocalItems {
	const LOCAL_ITEMS = {
		french: m.french(),
		english: m.english(),
		arabic: m.arabic(),
		portuguese: m.portuguese(),
		spanish: m.spanish(),
		german: m.german(),
		dutch: m.dutch(),
		italian: m.italian(),
		polish: m.polish(),
		home: m.home(),
		edit: m.edit(),
		overview: m.overview(),
		context: m.context(),
		governance: m.governance(),
		risk: m.risk(),
		compliance: m.compliance(),
		organization: m.organization(),
		extra: m.extra(),
		advanced: m.advanced(),
		analytics: m.analytics(),
		calendar: m.calendar(),
		threats: m.threats(),
		referenceControls: m.referenceControls(),
		appliedControls: m.appliedControls(),
		assets: m.assets(),
		asset: m.asset(),
		policies: m.policies(),
		riskMatrices: m.riskMatrices(),
		riskAssessments: m.riskAssessments(),
		riskScenarios: m.riskScenarios(),
		riskScenario: m.riskScenario(),
		riskAcceptances: m.riskAcceptances(),
		riskAcceptance: m.riskAcceptance(),
		complianceAssessments: m.complianceAssessments(),
		complianceAssessment: m.complianceAssessment(),
		evidences: m.evidences(),
		evidence: m.evidence(),
		frameworks: m.frameworks(),
		domains: m.domains(),
		projects: m.projects(),
		users: m.users(),
		user: m.user(),
		userGroups: m.userGroups(),
		roleAssignments: m.roleAssignments(),
		xRays: m.xRays(),
		scoringAssistant: m.scoringAssistant(),
		libraries: m.libraries(),
		backupRestore: m.backupRestore(),
		myProfile: m.myProfile(),
		aboutCiso: m.aboutCiso(),
		Logout: m.Logout(),
		name: m.name(),
		description: m.description(),
		parentDomain: m.parentDomain(),
		ref: m.ref(),
		refId: m.refId(),
		businessValue: m.businessValue(),
		email: m.email(),
		firstName: m.firstName(),
		lastName: m.lastName(),
		category: m.category(),
		eta: m.eta(),
		referenceControl: m.referenceControl(),
		appliedControl: m.appliedControl(),
		provider: m.provider(),
		domain: m.domain(),
		urn: m.urn(),
		id: m.id(),
		treatmentStatus: m.treatmentStatus(),
		currentLevel: m.currentLevel(),
		residualLevel: m.residualLevel(),
		riskMatrix: m.riskMatrix(),
		project: m.project(),
		folder: m.folder(),
		riskAssessment: m.riskAssessment(),
		threat: m.threat(),
		framework: m.framework(),
		file: m.file(),
		language: m.language(),
		builtin: m.builtin(),
		status: m.status(),
		effort: m.effort(),
		impact: m.impact(),
		expiryDate: m.expiryDate(),
		link: m.link(),
		createdAt: m.createdAt(),
		updatedAt: m.updatedAt(),
		acceptedAt: m.acceptedAt(),
		rejectedAt: m.rejectedAt(),
		revokedAt: m.revokedAt(),
		accepted: m.accept(),
		rejected: m.rejected(),
		revoked: m.revoked(),
		submitted: m.submitted(),
		locale: m.locale(),
		defaultLocale: m.defaultLocale(),
		annotation: m.annotation(),
		library: m.library(),
		typicalEvidence: m.typicalEvidence(),
		parentAsset: m.parentAsset(),
		parentAssets: m.parentAssets(),
		approver: m.approver(),
		state: m.state(),
		justification: m.justification(),
		parentFolder: m.parentFolder(),
		contentType: m.contentType(),
		type: m.type(),
		lcStatus: m.lcStatus(),
		internalReference: m.internalReference(),
		isActive: m.isActive(),
		dateJoined: m.dateJoined(),
		version: m.version(),
		treatment: m.treatment(),
		rid: m.rid(),
		currentProba: m.currentProba(),
		currentImpact: m.currentImpact(),
		residualProba: m.residualProba(),
		residualImpact: m.residualImpact(),
		existingControls: m.existingControls(),
		strengthOfKnowledge: m.strengthOfKnowledge(),
		dueDate: m.dueDate(),
		attachment: m.attachment(),
		observation: m.observation(),
		planned: m.planned(),
		active: m.active(),
		inactive: m.inactive(),
		addThreat: m.addThreat(),
		addReferenceControl: m.addReferenceControl(),
		addAppliedControl: m.addAppliedControl(),
		addAsset: m.addAsset(),
		addRiskAssessment: m.addRiskAssessment(),
		addRiskScenario: m.addRiskScenario(),
		addRiskAcceptance: m.addRiskAcceptance(),
		addComplianceAssessment: m.addComplianceAssessment(),
		addEvidence: m.addEvidence(),
		addDomain: m.addDomain(),
		addProject: m.addProject(),
		addUser: m.addUser(),
		addPolicy: m.addPolicy(),
		associatedThreats: m.associatedThreats(),
		associatedReferenceControls: m.associatedReferenceControls(),
		associatedAppliedControls: m.associatedAppliedControls(),
		associatedAssets: m.associatedAssets(),
		associatedRiskAssessments: m.associatedRiskAssessments(),
		associatedRiskScenarios: m.associatedRiskScenarios(),
		associatedRiskAcceptances: m.associatedRiskAcceptances(),
		associatedComplianceAssessments: m.associatedComplianceAssessments(),
		associatedEvidences: m.associatedEvidences(),
		associatedDomains: m.associatedDomains(),
		associatedProjects: m.associatedProjects(),
		associatedUsers: m.associatedUsers(),
		changePassword: m.changePassword(),
		label: m.label(),
		NA: m.NA(),
		threatAgentFactors: m.threatAgentFactors(),
		vulnerabilityFactors: m.vulnerabilityFactors(),
		businessImpactFactors: m.businessImpactFactors(),
		technicalImpactFactors: m.technicalImpactFactors(),
		assessmentVector: m.assessmentVector(),
		skillLevelText: m.skillLevelText(),
		skillLevelChoice1: m.skillLevelChoice1(),
		skillLevelChoice2: m.skillLevelChoice2(),
		skillLevelChoice3: m.skillLevelChoice3(),
		skillLevelChoice4: m.skillLevelChoice4(),
		skillLevelChoice5: m.skillLevelChoice5(),
		motiveText: m.motiveText(),
		motiveChoice1: m.motiveChoice1(),
		motiveChoice2: m.motiveChoice2(),
		motiveChoice3: m.motiveChoice3(),
		opportunityText: m.opportunityText(),
		opportunityChoice1: m.opportunityChoice1(),
		opportunityChoice2: m.opportunityChoice2(),
		opportunityChoice3: m.opportunityChoice3(),
		opportunityChoice4: m.opportunityChoice4(),
		sizeText: m.sizeText(),
		sizeChoice1: m.sizeChoice1(),
		sizeChoice2: m.sizeChoice2(),
		sizeChoice3: m.sizeChoice3(),
		sizeChoice4: m.sizeChoice4(),
		sizeChoice5: m.sizeChoice5(),
		easeOfDiscoveryText: m.easeOfDiscoveryText(),
		easeOfDiscoveryChoice1: m.easeOfDiscoveryChoice1(),
		easeOfDiscoveryChoice2: m.easeOfDiscoveryChoice2(),
		easeOfDiscoveryChoice3: m.easeOfDiscoveryChoice3(),
		easeOfDiscoveryChoice4: m.easeOfDiscoveryChoice4(),
		easeOfExploitText: m.easeOfExploitText(),
		easeOfExploitChoice1: m.easeOfExploitChoice1(),
		easeOfExploitChoice2: m.easeOfExploitChoice2(),
		easeOfExploitChoice3: m.easeOfExploitChoice3(),
		easeOfExploitChoice4: m.easeOfExploitChoice4(),
		awarenessText: m.awarenessText(),
		awarenessChoice1: m.awarenessChoice1(),
		awarenessChoice2: m.awarenessChoice2(),
		awarenessChoice3: m.awarenessChoice3(),
		awarenessChoice4: m.awarenessChoice4(),
		intrusionDetectionText: m.intrusionDetectionText(),
		intrusionDetectionChoice1: m.intrusionDetectionChoice1(),
		intrusionDetectionChoice2: m.intrusionDetectionChoice2(),
		intrusionDetectionChoice3: m.intrusionDetectionChoice3(),
		intrusionDetectionChoice4: m.intrusionDetectionChoice4(),
		financialDamageText: m.financialDamageText(),
		financialDamageChoice1: m.financialDamageChoice1(),
		financialDamageChoice2: m.financialDamageChoice2(),
		financialDamageChoice3: m.financialDamageChoice3(),
		financialDamageChoice4: m.financialDamageChoice4(),
		reputationDamageText: m.reputationDamageText(),
		reputationDamageChoice1: m.reputationDamageChoice1(),
		reputationDamageChoice2: m.reputationDamageChoice2(),
		reputationDamageChoice3: m.reputationDamageChoice3(),
		reputationDamageChoice4: m.reputationDamageChoice4(),
		nonComplianceText: m.nonComplianceText(),
		nonComplianceChoice1: m.nonComplianceChoice1(),
		nonComplianceChoice2: m.nonComplianceChoice2(),
		nonComplianceChoice3: m.nonComplianceChoice3(),
		nonComplianceChoice4: m.nonComplianceChoice4(),
		privacyViolationText: m.privacyViolationText(),
		privacyViolationChoice1: m.privacyViolationChoice1(),
		privacyViolationChoice2: m.privacyViolationChoice2(),
		privacyViolationChoice3: m.privacyViolationChoice3(),
		privacyViolationChoice4: m.privacyViolationChoice4(),
		lossOfConfidentialityText: m.lossOfConfidentialityText(),
		lossOfConfidentialityChoice1: m.lossOfConfidentialityChoice1(),
		lossOfConfidentialityChoice2: m.lossOfConfidentialityChoice2(),
		lossOfConfidentialityChoice3: m.lossOfConfidentialityChoice3(),
		lossOfConfidentialityChoice4: m.lossOfConfidentialityChoice4(),
		lossOfIntegrityText: m.lossOfIntegrityText(),
		lossOfIntegrityChoice1: m.lossOfIntegrityChoice1(),
		lossOfIntegrityChoice2: m.lossOfIntegrityChoice2(),
		lossOfIntegrityChoice3: m.lossOfIntegrityChoice3(),
		lossOfIntegrityChoice4: m.lossOfIntegrityChoice4(),
		lossOfIntegrityChoice5: m.lossOfIntegrityChoice5(),
		lossOfAvailabilityText: m.lossOfAvailabilityText(),
		lossOfAvailabilityChoice1: m.lossOfAvailabilityChoice1(),
		lossOfAvailabilityChoice2: m.lossOfAvailabilityChoice2(),
		lossOfAvailabilityChoice3: m.lossOfAvailabilityChoice3(),
		lossOfAvailabilityChoice4: m.lossOfAvailabilityChoice4(),
		lossOfAccountabilityText: m.lossOfAccountabilityText(),
		lossOfAccountabilityChoice1: m.lossOfAccountabilityChoice1(),
		lossOfAccountabilityChoice2: m.lossOfAccountabilityChoice2(),
		lossOfAccountabilityChoice3: m.lossOfAccountabilityChoice3(),
		undefined: m.undefined(),
		production: m.production(),
		development: m.development(),
		design: m.design(),
		endOfLife: m.endOfLife(),
		dropped: m.dropped(),
		technical: m.technical(),
		physical: m.physical(),
		veryLow: m.veryLow(),
		low: m.low(),
		high: m.high(),
		veryHigh: m.veryHigh(),
		small: m.small(),
		medium: m.medium(),
		large: m.large(),
		extraLarge: m.extraLarge(),
		policy: m.policy(),
		process: m.process(),
		composer: m.composer(),
		plan: m.plan(),
		open: m.open(),
		mitigate: m.mitigate(),
		accept: m.accept(),
		transfer: m.transfer(),
		avoid: m.avoid(),
		primary: m.primary(),
		support: m.support(),
		toDo: m.toDo(),
		inProgress: m.inProgress(),
		inReview: m.inReview(),
		deprecated: m.deprecated(),
		done: m.done(),
		nonCompliant: m.nonCompliant(),
		partiallyCompliant: m.partiallyCompliant(),
		requirementAssessments: m.requirementAssessments(),
		compliant: m.compliant(),
		notApplicable: m.notApplicable(),
		administrator: m.administrator(),
		analyst: m.analyst(),
		reader: m.reader(),
		domainManager: m.domainManager(),
		authors: m.authors(),
		reviewers: m.reviewers(),
		isPublished: m.isPublished(),
		noFileDetected: m.noFileDetected(),
		rankingScore: m.rankingScore(),
		'--SOK': m.undefinedSOK(),
		lowSOK: m.lowSOK(),
		mediumSOK: m.mediumSOK(),
		highSOK: m.highSOK(),
		libraryLoadingError: m.libraryLoadingError(),
		libraryAlreadyExistsError: m.libraryAlreadyLoadedError(),
		invalidLibraryFileError: m.invalidLibraryFileError(),
		libraryNotFound: m.libraryNotFound(),
		libraryHasNoUpdate: m.libraryHasNoUpdate(),
		dependencyNotFound: m.dependencyNotFound(),
		invalidLibraryUpdate: m.invalidLibraryUpdate(),
		minScore: m.minScore(),
		maxScore: m.maxScore(),
		scoresDefinition: m.scoresDefinition(),
		selectedImplementationGroups: m.selectedImplementationGroups(),
		implementationGroupsDefinition: m.implementationGroupsDefinition(),
		attemptToDeleteOnlyAdminAccountError: m.attemptToDeleteOnlyAdminAccountError(),
		attemptToRemoveOnlyAdminUserGroup: m.attemptToRemoveOnlyAdminUserGroup(),
		actionPlan: m.actionPlan(),
		matchingRequirements: m.matchingRequirements(),
		remediationPlan: m.remediationPlan(),
		incoming: m.incoming(),
		today: m.today(),
		outdated: m.outdated(),
		flashMode: m.flashMode(),
		complianceAssessmentInProgress: m.complianceAssessmentInProgress(),
		complianceAssessmentNoAuthor: m.complianceAssessmentNoAuthor(),
		requirementAssessmentNoAppliedControl: m.requirementAssessmentNoAppliedControl(),
		appliedControlNoReferenceControl: m.appliedControlNoReferenceControl(),
		evidenceNoFile: m.evidenceNoFile(),
		riskAssessmentInProgress: m.riskAssessmentInProgress(),
		riskAssessmentNoAuthor: m.riskAssessmentNoAuthor(),
		riskAssessmentEmpty: m.riskAssessmentEmpty(),
		riskScenarioNoCurrentLevel: m.riskScenarioNoCurrentLevel(),
		riskScenarioNoResidualLevel: m.riskScenarioNoResidualLevel(),
		riskScenarioResidualHigherThanCurrent: m.riskScenarioResidualHigherThanCurrent(),
		riskScenarioResidualProbaHigherThanCurrent: m.riskScenarioResidualProbaHigherThanCurrent(),
		riskScenarioResidualImpactHigherThanCurrent: m.riskScenarioResidualImpactHigherThanCurrent(),
		riskScenarioResidualLoweredWithoutMeasures: m.riskScenarioResidualLoweredWithoutMeasures(),
		riskScenarioAcceptedNoAcceptance: m.riskScenarioAcceptedNoAcceptance(),
		appliedControlNoETA: m.appliedControlNoETA(),
		appliedControlETAInPast: m.appliedControlETAInPast(),
		appliedControlNoEffort: m.appliedControlNoEffort(),
		appliedControlNoLink: m.appliedControlNoLink(),
		riskAcceptanceNoExpiryDate: m.riskAcceptanceNoExpiryDate(),
		riskAcceptanceExpired: m.riskAcceptanceExpired()
	};
	return LOCAL_ITEMS;
}
