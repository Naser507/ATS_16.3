# ATS_16.3 – Audio Processing Toolkit

ATS_16 is a modular audio processing system designed to explore real-world signal handling through a hybrid architecture combining Python-based orchestration with a C++ audio processing engine. The project focuses on building a scalable framework for audio conversion, session management, and event-driven UI workflows.

The system is being actively developed as part of an iterative engineering process. Current progress includes the core architecture, modular file operation system, and initial engine integration. Development is ongoing, with some components temporarily paused due to external constraints, while the overall design and system structure continue to evolve.

## Project Structure

```
.
├── Assets
├── bin
│   ├── app.py
│   ├── audio_converter
│   ├── config
│   │   ├── last_audio_path.json
│   │   └── session_cache.json
│   ├── dynamicLoader.py
│   ├── Engine
│   │   ├── audio_converter.cpp
│   │   └── events.json
│   ├── EventManager.py
│   ├── SessionManager.py
│   ├── Shared_Lib
│   ├── src
│   │   ├── app_exit.py
│   │   ├── appMainFrame.py
│   │   ├── audio_temp_manager.py
│   │   ├── bottomPanelEmpty.py
│   │   ├── file_convert_audio.py
│   │   ├── file_new_audio.py
│   │   ├── file_remove_audio.py
│   │   ├── file_save_audio.py
│   │   ├── layer1_menuStrip.py
│   │   ├── layer2_topPanel.py
│   │   ├── layer3_bottomPanel_class.py
│   │   ├── layer4_bottomRightButtons.py
│   │   ├── menu_file.py
│   │   ├── run_message.py
│   │   ├── save_message.py
│   │   ├── test_step.py
│   │   └── topPanel.py
├── Build
├── config
│   └── logs
├── Notes
│   ├── issues.txt
│   ├── MyInstructions.txt
│   └── YourFeedback.txt
├── Releases
├── scripts
├── tests
```

## Tech Stack

* Python (core application logic & UI)
* C++ (audio processing engine)
* Event-driven modular architecture
* JSON-based configuration system
