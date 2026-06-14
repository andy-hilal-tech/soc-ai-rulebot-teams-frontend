# SOC AI Rulebot Teams Frontend

This project is the Microsoft Teams frontend for the SOC AI Rulebot system.

## Purpose
This frontend receives user messages inside Microsoft Teams and forwards them to the deployed Rulebot backend API.

## Architecture
Teams SDK frontend
→ HTTPS POST to backend `/message`
→ backend returns response
→ frontend sends response back to Teams

## Current backend endpoint
`https://soc-ai-rulebot-agent.livelyocean-c3150e2c.swedencentral.azurecontainerapps.io/message`

## Notes
- This repo contains only the Teams-facing frontend.
- Backend logic, rule analysis, offense analysis, and RAG live in the separate backend repo.
- Local Python virtual environment (`.venv`) is excluded from source control.