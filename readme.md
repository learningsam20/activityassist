# Requirements

This project is useful for building AI powered user monitoring system. Here are the key requirements:

## Background agent running on client's machine

- It must have an agent that can monitor user activity
- It must store the screenshot of user's activity in a folder
- It must store other details like mouse, keyboad positions, app accessed, app type, etc. along wit the screenshots
- It must be able to run in background
- The storage needs to be configurable to any s3 proxy compatible storage or local storage

## Analytics app running on server

- The app must be able to identify subsequences/ patterns of user activity based on screenshots series and/or the keystrokes captured by the agent
- It needs to generate a SOP document based on the images captured
- It should draw a pareto diagram indicating contribution of each cluster of activities
- It should also propose a name to these clusters based on the images and/or keystrokes contained within
- Once the patterns are approved by the SME, it should be able to compare the new images with the cluster to identify anomalies if any
- It should provide optimization suggestions based on the above comparison

## Technology stack

- Python, FastAPI
- React/Angular for UI
- Postgre for database (to begin with sqlite is okay too)
- Storage can be local or s3 proxy compatible storage
- Use Ollama for LLM

## Additional requirements

- Agent footprint should be low
- Image comparison and clustering into sequences needs to be efficient
- UX has to be rich, modern, should support dark and light mode
- Should have user login (for now local, but should later on be SSO/keycloak based)
- Intelligent insights using LLM/AI agents should be present for most data collected across Ux. i.e. it needs to be an AI first experience
- Keep backend API in api folder, frontend in frontned folder, agent in monitor folder and AI agent in ai folder
- Keep anything configurable in .env file