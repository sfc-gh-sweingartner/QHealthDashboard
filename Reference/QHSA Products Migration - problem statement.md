QHSA Products Migration - Problem Statement
Current Challenge
Quantium's health analytics products (Q.Checkup, Q.Checkup Lite, Q.Dose) are experiencing
significant performance issues on our current Tableau on-premises infrastructure. Q.Checkup, our
most comprehensive dashboard, takes 40-50 seconds to load, creating poor user experience and
limiting product scalability
Q.Hospitals is a new build in PowerBI Pro, and is expected to require complex enhancements in the
next iteration that will likely require a larger dataset to support these enhancements
Tableau requires high-touch support for even simple user requirements like resetting a password
PowerBI Pro requires complex user onboarding when clients have their own PowerBI licences
PowerBI Pro has limitations on size of underlying dataset (must be less than 1GB) and costs escalate
significantly (2-3x) for PowerBI Fabric
Technical Context
Data pipeline: Discovery → Azure → Snowflake → Tableau visualization (PowerBI for Q.Hospitals)
Current infrastructure: Tableau on-premises across 9 servers, 3 environments. PowerBI Pro for
Q.Hospitals.
Dataset sizes: 1.5-3GB per product
Migration Objectives
Our solution must prioritise four critical factors:
1. Cost Optimisation: Reduce overall platform costs while eliminating expensive on-premises
infrastructure maintenance
2. AI Integration: Enable opportunity to align with Quantium's AI strategy, including ability to explore
natural language querying and advanced analytics capabilities. This will also create an opportunity for
premium pricing tiers for access to AI-enhanced capabilities
3. Scalability: Support expected 5-10x subscription growth, rapid product evolution and handle
growing data volumes without performance degradation and concurrency issues
4. Capability for user self-service: Support expected subscription growth without requiring
proportional scaling of support team, by enabling more self-service functionality
Technical Requirements
Improve current 40-50 second load times to under 5 seconds
Maintain user experience during transition

Support web-based access (primarily desktop users)
Constraints
Need to maintain current functionality during migration
Looking for modern web-based solutions rather than traditional BI tools
New Tableau on-prem licence will expire in September 2026 and we would ideally not want to renew
Current Considerations
Feature freeze under consideration for existing products to address performance issues
Evaluating multiple migration options including Tableau Cloud, Power BI, native web-app, and
potential Snowflake-based solutions
Desired Outcome
Implement a cost-effective, AI-enabled, scalable solution that reduces dashboard load times from 40-50
seconds to under 5 seconds while positioning our products for 5-10x subscription growth. The solution
must support our AI transformation strategy, reduce operational overhead by eliminating on-premises
infrastructure, and enable new revenue opportunities through enhanced capabilities. Success will be
measured by improved client satisfaction, reduced support requests, accelerated onboarding of new
clients, and migration of all Q.Checkup clients to the new platform by end of FY26 (June 2026).