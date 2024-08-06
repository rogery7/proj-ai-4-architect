# Custom Agent Workflow System

## Overview

This project demonstrates a flexible system for creating and managing custom agents to automate various workflow tasks. It showcases the ability to develop new custom agents that match specific workflow needs, including automating repetitive tasks, integrating with APIs, and creating specialized commands.

The system utilizes a main orchestrator agent that delegates tasks to specialized agents, each designed for specific functions:

1. **Tech Spec Writer Agent**: Generates detailed technical specifications for projects.
2. **D2 Diagram Agent**: Creates D2 diagrams to visualize project architecture and components.
3. **Jira Ticket Creator Agent**: Generates Jira ticket definitions based on project specifications and diagrams.

## Projects Created

The system has been used to create comprehensive project setups for two applications:

### 1. GlobalWarming

An interactive web application designed to educate users about climate change and its impacts.

Key Features:

- Real-time global temperature data visualization
- Interactive maps showing climate change effects by region
- Personal carbon footprint calculator
- Tips for reducing individual environmental impact

Project Artifacts:

- **README.md**: Detailed technical specification including:
  - Data sources for climate information
  - Backend architecture for data processing and storage
  - Frontend design for interactive visualizations
  - API integrations with climate databases
- **diagram.d2**: Architecture diagram illustrating:
  - Data flow from climate databases to the application
  - User interaction components
  - Backend services for data processing and analysis
- **JIRA_TICKETS.md**: Development tasks including:
  - Setting up data pipelines for climate information
  - Implementing interactive map features
  - Developing the carbon footprint calculator algorithm
  - Creating educational content on climate change mitigation

### 2. WaterTracker

A mobile application helping users maintain proper hydration by tracking daily water intake.

Key Features:

- Personalized daily water intake goals based on user metrics
- Easy-to-use interface for logging water consumption
- Customizable reminders to drink water throughout the day
- Progress visualizations and achievement system

Project Artifacts:

- **README.md**: Technical specification detailing:
  - User profile management and goal-setting algorithms
  - Local data storage for offline functionality
  - Notification system for hydration reminders
  - Integration with health apps for comprehensive health tracking
- **diagram.d2**: System architecture diagram showing:
  - User interface components for water logging and goal tracking
  - Backend services for data management and goal calculations
  - Integration points with device notification systems and health apps
- **JIRA_TICKETS.md**: Development tasks including:
  - Implementing the water intake logging interface
  - Developing the algorithm for personalized hydration goals
  - Creating the notification and reminder system
  - Designing and implementing progress visualizations and achievements

These projects demonstrate the system's ability to generate comprehensive project documentation, architecture diagrams, and development task lists for diverse applications, from educational platforms to personal health tools.
