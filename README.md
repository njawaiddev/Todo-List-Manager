# Todo List Manager

A modern, cross-platform Todo List application built with Python and Tkinter. Features a dark theme, date/time scheduling, and task alerts.

![Todo List Manager Screenshot](screenshots/app_screenshot.png)

## Features

- 🌓 Modern dark theme interface
- 📅 Calendar and time picker for task scheduling
- ⏰ Task alerts and notifications
- ✅ Mark tasks as complete
- 🗑️ Delete completed tasks
- 📊 Sort tasks by due date
- 💾 Automatic task saving
- 🔔 Alert notifications for upcoming and overdue tasks

## Installation


### Building from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/todo-list-manager.git
cd todo-list-manager
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application:
```bash
python todo_app.py
```

### Building Executables

#### For macOS:
```bash
chmod +x build_macos.sh
./build_macos.sh
```

#### For Windows:
```bash
build_windows.bat
```

## Development

### Project Structure
```
todo-list-manager/
├── todo_app.py          # Main application file
├── requirements.txt     # Python dependencies
├── setup.py            # Setup configuration
├── todo_app.spec       # PyInstaller specification
├── build_macos.sh      # macOS build script
└── build_windows.bat   # Windows build script
```

### Requirements
- Python 3.8 or higher
- tkinter (usually comes with Python)
- tkcalendar
- PyInstaller (for building executables)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
