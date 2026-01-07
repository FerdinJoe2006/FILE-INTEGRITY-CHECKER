🛡️ File Integrity Checker (Python)

A Python-based File Integrity Monitoring (FIM) tool that helps detect unauthorized or accidental file modifications using cryptographic hash verification.
This project securely tracks file changes, deletions, and integrity status through a simple command-line interface.

🚀 Features

🔐 SHA-256 hash-based integrity verification

📁 Register files for continuous monitoring

🔍 Detect file modifications, deletions, and size changes

🗂️ Persistent integrity database using JSON

🔄 Update baseline hashes when changes are expected

📊 Full system scan with summarized results

🖥️ User-friendly menu-driven CLI

📂 Project Structure
File-Integrity-Checker/
│
├── integrity_database.json   # Auto-generated integrity database
├── file_integrity_checker.py # Main Python application
└── README.md                 # Project documentation

⚙️ Requirements

Python 3.7 or higher

No external libraries required (uses Python standard library only)

▶️ How to Run

Clone the repository

git clone https://github.com/your-username/file-integrity-checker.git
cd file-integrity-checker


Run the program

python file_integrity_checker.py

🧭 Menu Options
Option	Description
1	Register a new file for monitoring
2	Check integrity of a specific file
3	Scan all monitored files
4	List all monitored files
5	Update baseline hash for a modified file
6	Remove a file from monitoring
7	Exit the program
📝 How It Works

When a file is registered, its SHA-256 hash, size, and timestamp are stored.

On each integrity check:

The file is re-hashed

Hashes and sizes are compared

Status is updated as:

intact

modified

deleted

All records are saved in integrity_database.json.

📌 Example Use Cases

Detect unauthorized changes to critical system files

Monitor configuration or log files

Educational demonstration of cryptographic hashing

Basic intrusion detection support

🔐 Security Notes

Uses SHA-256, a secure cryptographic hashing algorithm

Reads files in chunks to efficiently handle large files

Absolute paths prevent duplicate or ambiguous file tracking

🧪 Sample Output
✓ File intact: config.txt
⚠ ALERT: File modified: data.json
⚠ WARNING: File 'logs.txt' has been deleted!

📜 License

This project is open-source and available under the MIT License.

👨‍💻 Author

CODTECH Project
Built to demonstrate file integrity monitoring using Python.

⭐ Future Enhancements (Optional)

Directory monitoring

Real-time background monitoring

Email or system alerts

Cross-platform service mode

Encryption for integrity database
