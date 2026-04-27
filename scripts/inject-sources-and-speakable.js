const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, '../blog');

// Official government sources per post
const SOURCES = {
  'acra-nominee-director-changes-2026': [
    { name: 'ACRA – Nominee Director Regulations', url: 'https://www.acra.gov.sg/legislation/acts-and-subsidiary-legislation/companies-act/companies-act-amendments' },
    { name: 'ACRA – Register of Nominee Directors (ROND)', url: 'https://www.acra.gov.sg/business/running-a-business/nominee-directors' },
    { name: 'ACRA – Registered Filing Agents', url: 'https://www.acra.gov.sg/business/filing-agents' },
  ],
  'ai-startups-incorporating-singapore-2026': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'AI Singapore (AISG)', url: 'https://aisingapore.org/' },
    { name: 'EnterpriseSG – Startup SG', url: 'https://www.enterprisesg.gov.sg/grow-your-business/startup-sg' },
    { name: 'IMDA – Digital Industry Singapore', url: 'https://www.imda.gov.sg/business-and-technology/industry-development' },
  ],
  'becoming-nri-singapore-tax-ep-costs': [
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'IRAS – Tax Residency for Individuals', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/basics-of-individual-income-tax/tax-residency-and-tax-rates' },
    { name: 'MOM – Personalised Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/personalised-employment-pass' },
  ],
  'best-company-incorporation-services-singapore': [
    { name: 'ACRA – Registered Filing Agents', url: 'https://www.acra.gov.sg/business/filing-agents' },
    { name: 'ACRA BizFile+', url: 'https://www.bizfile.gov.sg/' },
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
  ],
  'can-foreigner-start-business-singapore': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'MOM – EntrePass', url: 'https://www.mom.gov.sg/passes-and-permits/entrepass' },
    { name: 'EDB – Why Singapore', url: 'https://www.edb.gov.sg/en/why-singapore.html' },
    { name: 'EnterpriseSG – Startup SG Founder', url: 'https://www.enterprisesg.gov.sg/grow-your-business/startup-sg/startup-sg-founder' },
  ],
  'corporate-secretary-singapore-what-they-do': [
    { name: 'ACRA – Company Secretary Requirements', url: 'https://www.acra.gov.sg/business/running-a-business/company-secretary' },
    { name: 'ACRA – Annual Return Filing', url: 'https://www.acra.gov.sg/business/running-a-business/annual-return' },
    { name: 'Companies Act (Cap. 50)', url: 'https://sso.agc.gov.sg/Act/CoA1967' },
  ],
  'cost-of-incorporating-company-singapore': [
    { name: 'ACRA – Fees for Business Registration', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company/fees' },
    { name: 'ACRA BizFile+ – Name Application', url: 'https://www.bizfile.gov.sg/' },
    { name: 'IRAS – Corporate Income Tax Rates', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/basics-of-corporate-income-tax/corporate-income-tax-rate-rebates-and-tax-exemption-schemes' },
  ],
  'fema-rbi-compliance-indian-founders-singapore': [
    { name: 'RBI – Overseas Investment Rules 2022', url: 'https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=54073' },
    { name: 'FEMA – Foreign Exchange Management Act', url: 'https://rbi.org.in/Scripts/Acts_Amended.aspx?id=1' },
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
  ],
  'gulf-family-offices-singapore-vcc': [
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'MAS – Fund Management Licensing', url: 'https://www.mas.gov.sg/regulation/capital-markets/fund-management' },
    { name: 'ACRA – Setting Up a VCC', url: 'https://www.acra.gov.sg/business/setting-up-a-variable-capital-company' },
    { name: 'IRAS – 13O and 13U Tax Incentives', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
  ],
  'how-long-does-singapore-company-incorporation-take': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'ACRA BizFile+', url: 'https://www.bizfile.gov.sg/' },
    { name: 'ACRA – Registered Filing Agents', url: 'https://www.acra.gov.sg/business/filing-agents' },
  ],
  'how-to-close-company-singapore': [
    { name: 'ACRA – Closing a Local Company (Strike Off)', url: 'https://www.acra.gov.sg/business/closing-a-local-company' },
    { name: 'ACRA – Winding Up a Company', url: 'https://www.acra.gov.sg/business/closing-a-local-company/winding-up' },
    { name: 'IRAS – Corporate Tax Clearance', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/dormant-companies-or-companies-closing-down/tax-for-companies-closing-down' },
  ],
  'how-to-incorporate-company-singapore-foreigner': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'ACRA BizFile+', url: 'https://www.bizfile.gov.sg/' },
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'EDB – Doing Business in Singapore', url: 'https://www.edb.gov.sg/en/setting-up-in-singapore.html' },
  ],
  'how-to-incorporate-vcc-singapore': [
    { name: 'MAS – Variable Capital Companies Framework', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'ACRA – Setting Up a VCC', url: 'https://www.acra.gov.sg/business/setting-up-a-variable-capital-company' },
    { name: 'IRAS – Tax Incentives for Funds (13O/13U)', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
  ],
  'india-vs-singapore-tax-founders': [
    { name: 'IRAS – Corporate Income Tax Rate', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/basics-of-corporate-income-tax/corporate-income-tax-rate-rebates-and-tax-exemption-schemes' },
    { name: 'IRAS – Individual Income Tax Rates', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/basics-of-individual-income-tax/tax-residency-and-tax-rates/individual-income-tax-rates' },
    { name: 'IRAS – Singapore–India Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
  ],
  'mas-vcc-thematic-review-2025': [
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'MAS – AML/CFT Requirements for VCCs', url: 'https://www.mas.gov.sg/regulation/anti-money-laundering' },
    { name: 'ACRA – VCC Annual Return', url: 'https://www.acra.gov.sg/business/running-a-business/annual-return' },
  ],
  'nominee-director-singapore-complete-guide': [
    { name: 'ACRA – Nominee Director Regulations', url: 'https://www.acra.gov.sg/business/running-a-business/nominee-directors' },
    { name: 'Companies Act – Director Duties (s157)', url: 'https://sso.agc.gov.sg/Act/CoA1967' },
    { name: 'ACRA – Registered Filing Agents', url: 'https://www.acra.gov.sg/business/filing-agents' },
  ],
  'oecd-pillar-two-singapore-holding-company': [
    { name: 'IRAS – BEPS Pillar Two Implementation', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/specific-topics/beps' },
    { name: 'OECD – Pillar Two Global Minimum Tax', url: 'https://www.oecd.org/tax/beps/pillar-two/' },
    { name: 'IRAS – Corporate Income Tax Rate', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/basics-of-corporate-income-tax/corporate-income-tax-rate-rebates-and-tax-exemption-schemes' },
  ],
  'penalties-late-filing-singapore': [
    { name: 'ACRA – Enforcement and Penalties', url: 'https://www.acra.gov.sg/business/running-a-business/annual-return' },
    { name: 'IRAS – Penalties for Late Filing', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/filing-taxes-for-companies/filing-income-taxes-for-companies' },
    { name: 'MOM – CPF Compliance', url: 'https://www.cpf.gov.sg/employer/employer-obligations/paying-cpf-contributions' },
  ],
  'redomicile-cayman-fund-to-singapore-vcc': [
    { name: 'MAS – VCC Redomiciliation Framework', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'ACRA – VCC Registration', url: 'https://www.acra.gov.sg/business/setting-up-a-variable-capital-company' },
    { name: 'Variable Capital Companies Act', url: 'https://sso.agc.gov.sg/Act/VCCA2018' },
  ],
  'redomicile-difc-adgm-fund-to-singapore-vcc': [
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'ACRA – Setting Up a VCC', url: 'https://www.acra.gov.sg/business/setting-up-a-variable-capital-company' },
    { name: 'IRAS – 13O/13U Tax Incentives for Funds', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
  ],
  'relocating-business-uae-to-singapore': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'EDB – Why Singapore', url: 'https://www.edb.gov.sg/en/why-singapore.html' },
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'IRAS – Singapore–UAE Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
  ],
  'saudi-family-offices-singapore-vcc': [
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'IRAS – 13O/13U Tax Incentives', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
    { name: 'EDB – Family Office Programme', url: 'https://www.edb.gov.sg/en/our-industries/financial-services/family-offices.html' },
  ],
  'singapore-bank-account-foreign-company': [
    { name: 'MAS – Banking Regulation in Singapore', url: 'https://www.mas.gov.sg/regulation/banks' },
    { name: 'ACRA – Certificate of Incorporation', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'MAS – List of Licensed Banks', url: 'https://www.mas.gov.sg/regulation/banks/list-of-banks-in-singapore' },
  ],
  'singapore-company-annual-compliance-checklist': [
    { name: 'ACRA – Annual Return Filing', url: 'https://www.acra.gov.sg/business/running-a-business/annual-return' },
    { name: 'IRAS – Corporate Tax Filing (Form C-S)', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/filing-taxes-for-companies/filing-income-taxes-for-companies' },
    { name: 'IRAS – Estimated Chargeable Income (ECI)', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/filing-taxes-for-companies/estimated-chargeable-income-(eci)' },
    { name: 'CPF Board – Employer Obligations', url: 'https://www.cpf.gov.sg/employer/employer-obligations' },
  ],
  'singapore-company-incorporation-australian-founders': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'IRAS – Singapore–Australia Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
  ],
  'singapore-company-incorporation-chinese-hongkong-founders': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'IRAS – Singapore–China Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
    { name: 'EDB – Financial Services in Singapore', url: 'https://www.edb.gov.sg/en/our-industries/financial-services.html' },
  ],
  'singapore-company-incorporation-indian-founders': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'IRAS – Singapore–India Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
    { name: 'RBI – Overseas Investment Rules 2022', url: 'https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=54073' },
  ],
  'singapore-company-incorporation-indonesian-founders': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'IRAS – Singapore–Indonesia Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
  ],
  'singapore-company-incorporation-uk-founders': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'IRAS – Singapore–UK Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
  ],
  'singapore-company-incorporation-us-founders': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'EDB – Why Singapore for US Companies', url: 'https://www.edb.gov.sg/en/why-singapore.html' },
  ],
  'singapore-corporate-tax-guide-small-business': [
    { name: 'IRAS – Corporate Income Tax Rate', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/basics-of-corporate-income-tax/corporate-income-tax-rate-rebates-and-tax-exemption-schemes' },
    { name: 'IRAS – Start-Up Tax Exemption (SUTE)', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/start-up-tax-exemption-scheme' },
    { name: 'IRAS – Partial Tax Exemption', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/basics-of-corporate-income-tax/corporate-income-tax-rate-rebates-and-tax-exemption-schemes' },
    { name: 'IRAS – Filing Corporate Tax (Form C-S)', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/filing-taxes-for-companies/filing-income-taxes-for-companies' },
  ],
  'singapore-employment-pass-company-director': [
    { name: 'MOM – Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass' },
    { name: 'MOM – COMPASS Framework', url: 'https://www.mom.gov.sg/passes-and-permits/employment-pass/eligibility' },
    { name: 'MOM – Personalised Employment Pass', url: 'https://www.mom.gov.sg/passes-and-permits/personalised-employment-pass' },
    { name: 'MOM – EntrePass', url: 'https://www.mom.gov.sg/passes-and-permits/entrepass' },
  ],
  'singapore-flip-structure-indian-startups': [
    { name: 'RBI – Overseas Investment Rules 2022', url: 'https://rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=54073' },
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'IRAS – Singapore–India Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
  ],
  'singapore-holding-company-gulf-assets': [
    { name: 'IRAS – Holding Company Tax Exemptions', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/specific-topics/companies-receiving-foreign-income' },
    { name: 'IRAS – Singapore–UAE Double Tax Agreement', url: 'https://www.iras.gov.sg/taxes/individual-income-tax/employees/tax-treaties' },
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'EDB – Why Singapore', url: 'https://www.edb.gov.sg/en/why-singapore.html' },
  ],
  'singapore-political-stability-business-continuity': [
    { name: 'EDB – Why Singapore', url: 'https://www.edb.gov.sg/en/why-singapore.html' },
    { name: 'World Bank – Ease of Doing Business', url: 'https://www.worldbank.org/en/programs/business-enabling-environment' },
    { name: 'ACRA – Singapore Business Environment', url: 'https://www.acra.gov.sg/' },
  ],
  'singapore-pte-ltd-vs-sole-proprietor-llp': [
    { name: 'ACRA – Types of Business Structures', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'ACRA – Limited Liability Partnership', url: 'https://www.acra.gov.sg/business/setting-up-a-limited-liability-partnership' },
    { name: 'ACRA – Sole Proprietorship', url: 'https://www.acra.gov.sg/business/setting-up-a-sole-proprietorship-or-partnership' },
    { name: 'IRAS – Tax Treatment by Business Structure', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax' },
  ],
  'singapore-vs-dubai-company-incorporation': [
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'EDB – Why Singapore', url: 'https://www.edb.gov.sg/en/why-singapore.html' },
    { name: 'IRAS – Corporate Tax Rate', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/basics-of-corporate-income-tax/corporate-income-tax-rate-rebates-and-tax-exemption-schemes' },
  ],
  'umbrella-vcc-vs-standalone-singapore': [
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'Variable Capital Companies Act', url: 'https://sso.agc.gov.sg/Act/VCCA2018' },
    { name: 'ACRA – Setting Up a VCC', url: 'https://www.acra.gov.sg/business/setting-up-a-variable-capital-company' },
  ],
  'us-tariffs-singapore-company-incorporation': [
    { name: 'EDB – Why Singapore', url: 'https://www.edb.gov.sg/en/why-singapore.html' },
    { name: 'ACRA – Setting Up a Local Company', url: 'https://www.acra.gov.sg/business/setting-up-a-local-company' },
    { name: 'Singapore Customs – Free Trade Agreements', url: 'https://www.customs.gov.sg/businesses/customs-schemes-licences-framework/free-trade-zones' },
  ],
  'variable-capital-company-singapore-vcc': [
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'Variable Capital Companies Act', url: 'https://sso.agc.gov.sg/Act/VCCA2018' },
    { name: 'ACRA – Setting Up a VCC', url: 'https://www.acra.gov.sg/business/setting-up-a-variable-capital-company' },
    { name: 'IRAS – 13O/13U Tax Incentives', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
  ],
  'vcc-13o-13u-tax-incentives-singapore': [
    { name: 'IRAS – 13O Onshore Fund Tax Incentive', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
    { name: 'MAS – Fund Tax Incentive Schemes', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'Income Tax Act – Section 13O/13U', url: 'https://sso.agc.gov.sg/Act/ITA1947' },
  ],
  'vcc-annual-compliance-singapore': [
    { name: 'ACRA – VCC Annual Return', url: 'https://www.acra.gov.sg/business/running-a-business/annual-return' },
    { name: 'MAS – AML/CFT for VCCs', url: 'https://www.mas.gov.sg/regulation/anti-money-laundering' },
    { name: 'IRAS – 13O/13U Annual Conditions', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
  ],
  'vcc-compliance-requirements-singapore': [
    { name: 'MAS – VCC Regulatory Requirements', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'ACRA – VCC Annual Return', url: 'https://www.acra.gov.sg/business/running-a-business/annual-return' },
    { name: 'Variable Capital Companies Act', url: 'https://sso.agc.gov.sg/Act/VCCA2018' },
  ],
  'vcc-family-office-singapore-2025': [
    { name: 'EDB – Family Office in Singapore', url: 'https://www.edb.gov.sg/en/our-industries/financial-services/family-offices.html' },
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'IRAS – 13O/13U Tax Incentives', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
  ],
  'vcc-fund-administration-singapore': [
    { name: 'MAS – Fund Management Licensing', url: 'https://www.mas.gov.sg/regulation/capital-markets/fund-management' },
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'ACRA – VCC Requirements', url: 'https://www.acra.gov.sg/business/setting-up-a-variable-capital-company' },
  ],
  'vcc-singapore-vs-cayman-islands': [
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'Variable Capital Companies Act', url: 'https://sso.agc.gov.sg/Act/VCCA2018' },
    { name: 'IRAS – 13O/13U Fund Tax Incentives', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
  ],
  'when-to-register-gst-singapore': [
    { name: 'IRAS – GST Registration', url: 'https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/gst-registration-deregistration/do-i-need-to-register-for-gst' },
    { name: 'IRAS – GST Rate and Scope', url: 'https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/basics-of-gst/goods-and-services-tax-(gst)-what-it-is-and-how-it-works' },
    { name: 'IRAS – Voluntary GST Registration', url: 'https://www.iras.gov.sg/taxes/goods-services-tax-(gst)/gst-registration-deregistration/factors-to-consider-before-registering-voluntarily-for-gst' },
  ],
  'why-vcc-good-vehicle-for-funds-singapore': [
    { name: 'MAS – Variable Capital Companies', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'Variable Capital Companies Act', url: 'https://sso.agc.gov.sg/Act/VCCA2018' },
    { name: 'IRAS – 13O/13U Tax Incentives', url: 'https://www.iras.gov.sg/schemes/disbursement-schemes/tax-incentive-schemes-for-funds' },
    { name: 'EDB – Asset Management in Singapore', url: 'https://www.edb.gov.sg/en/our-industries/financial-services/asset-management.html' },
  ],
  'mas-vcc-thematic-review-2025': [
    { name: 'MAS – VCC Thematic Review', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'MAS – AML/CFT Notices', url: 'https://www.mas.gov.sg/regulation/anti-money-laundering' },
  ],
  'redomicile-cayman-fund-to-singapore-vcc': [
    { name: 'MAS – VCC Redomiciliation', url: 'https://www.mas.gov.sg/regulation/variable-capital-companies' },
    { name: 'Variable Capital Companies Act', url: 'https://sso.agc.gov.sg/Act/VCCA2018' },
  ],
  'nominee-director-singapore-complete-guide': [
    { name: 'ACRA – Nominee Directors', url: 'https://www.acra.gov.sg/business/running-a-business/nominee-directors' },
    { name: 'Companies Act – Director Duties', url: 'https://sso.agc.gov.sg/Act/CoA1967' },
  ],
  'penalties-late-filing-singapore': [
    { name: 'ACRA – Late Filing Penalties', url: 'https://www.acra.gov.sg/business/running-a-business/annual-return' },
    { name: 'IRAS – Late Filing and Payment Penalties', url: 'https://www.iras.gov.sg/taxes/corporate-income-tax/filing-taxes-for-companies/filing-income-taxes-for-companies' },
  ],
};

const dirs = fs.readdirSync(blogDir).filter(d =>
  fs.statSync(path.join(blogDir, d)).isDirectory()
);

let sourcesAdded = 0, speakableAdded = 0, skipped = 0;

for (const dir of dirs) {
  const filePath = path.join(blogDir, dir, 'index.html');
  if (!fs.existsSync(filePath)) continue;

  let html = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // 1. Inject speakable schema if missing
  if (!html.includes('"speakable"') && !html.includes('SpeakableSpecification')) {
    const speakable = `  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "speakable": {
      "@type": "SpeakableSpecification",
      "cssSelector": ["h1", ".article-body > p:first-child", ".article-faq-section .faq-answer p"]
    }
  }
  </script>`;
    html = html.replace('</head>', speakable + '\n</head>');
    speakableAdded++;
    changed = true;
  }

  // 2. Inject official sources section if missing
  const sources = SOURCES[dir];
  if (sources && !html.includes('article-sources-section')) {
    const links = sources.map(s =>
      `      <li><a href="${s.url}" target="_blank" rel="noopener noreferrer">${s.name} ↗</a></li>`
    ).join('\n');

    const section = `
      <section class="article-sources-section" style="margin-top:40px;padding-top:28px;border-top:1px solid var(--gray-200);">
        <h3 style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:var(--gray-500);margin-bottom:12px;">Official Sources</h3>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:6px;">
${links}
        </ul>
      </section>`;

    // Insert before the FAQ section (or before </article>)
    if (html.includes('article-faq-section')) {
      html = html.replace(
        '<section class="article-faq-section"',
        section + '\n      <section class="article-faq-section"'
      );
    } else {
      html = html.replace('</article>', section + '\n    </article>');
    }
    sourcesAdded++;
    changed = true;
  }

  if (changed) {
    fs.writeFileSync(filePath, html);
    console.log(`✓ ${dir}`);
  } else {
    skipped++;
  }
}

console.log(`\nSpeakable schema: ${speakableAdded} posts`);
console.log(`Official sources: ${sourcesAdded} posts`);
console.log(`Skipped (already done): ${skipped}`);
