# IT Notes — SOC AI Rulebot Teams Frontend

## What this app does
This Teams frontend receives messages from users in Microsoft Teams and forwards them to the deployed backend API.

## Backend target
`https://soc-ai-rulebot-agent.livelyocean-c3150e2c.swedencentral.azurecontainerapps.io/message`

## Security model
- Frontend contains no QRadar credentials
- Frontend contains no Azure OpenAI secrets
- Frontend acts only as a Teams-to-backend relay
- All analysis logic remains in the backend service

## Repo split
- Frontend repo: Teams app only
andy-hilal-tech/soc-ai-rulebot-teams-frontend
- Backend repo: analysis, RAG, rule lookup, offense analysis
andy-hilal-tech/soc-ai-rulebot-agent