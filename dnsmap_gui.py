import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
import subprocess

class DnsmapGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('dnsmap GUI')
        self.setGeometry(100, 100, 600, 500)
        self.setMinimumSize(600, 500)

        # Labels and LineEdits for options
        self.target_label = QLabel('Target Domain or IP:')
        self.target_edit = QLineEdit()
        self.target_edit.setToolTip('Enter the domain name or IP address to scan')

        self.wordlist_label = QLabel('Wordlist File:')
        self.wordlist_edit = QLineEdit()
        self.wordlist_edit.setToolTip('Path to the wordlist file (optional)')
        self.wordlist_button = QPushButton('Browse...')
        self.wordlist_button.clicked.connect(self.browse_wordlist)

        self.regular_results_label = QLabel('Regular Results File:')
        self.regular_results_edit = QLineEdit()
        self.regular_results_edit.setToolTip('Path to save regular results (optional)')
        self.regular_results_button = QPushButton('Browse...')
        self.regular_results_button.clicked.connect(self.browse_regular_results)

        self.csv_results_label = QLabel('CSV Results File:')
        self.csv_results_edit = QLineEdit()
        self.csv_results_edit.setToolTip('Path to save CSV results (optional)')
        self.csv_results_button = QPushButton('Browse...')
        self.csv_results_button.clicked.connect(self.browse_csv_results)

        self.delay_label = QLabel('Delay (ms):')
        self.delay_edit = QLineEdit()
        self.delay_edit.setToolTip('Delay between requests in milliseconds (optional)')

        self.ips_ignore_label = QLabel('IPs to Ignore:')
        self.ips_ignore_edit = QLineEdit()
        self.ips_ignore_edit.setToolTip('Comma-separated list of IPs to ignore (optional)')

        # Output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)

        # Button to execute dnsmap
        self.run_button = QPushButton('Run dnsmap')
        self.run_button.clicked.connect(self.run_dnsmap)

        # Button to clear output
        self.clear_button = QPushButton('Clear Output')
        self.clear_button.clicked.connect(self.output_display.clear)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.target_label)
        layout.addWidget(self.target_edit)
        layout.addWidget(self.wordlist_label)
        layout.addWidget(self.wordlist_edit)
        layout.addWidget(self.wordlist_button)
        layout.addWidget(self.regular_results_label)
        layout.addWidget(self.regular_results_edit)
        layout.addWidget(self.regular_results_button)
        layout.addWidget(self.csv_results_label)
        layout.addWidget(self.csv_results_edit)
        layout.addWidget(self.csv_results_button)
        layout.addWidget(self.delay_label)
        layout.addWidget(self.delay_edit)
        layout.addWidget(self.ips_ignore_label)
        layout.addWidget(self.ips_ignore_edit)
        layout.addWidget(self.run_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.output_display)

        self.setLayout(layout)
        self.show()

    def browse_wordlist(self):
        file_dialog = QFileDialog()
        wordlist_file, _ = file_dialog.getOpenFileName(self, "Select Wordlist File", "", "All Files (*)")
        if wordlist_file:
            self.wordlist_edit.setText(wordlist_file)

    def browse_regular_results(self):
        file_dialog = QFileDialog()
        regular_results_file, _ = file_dialog.getSaveFileName(self, "Select Regular Results File", "", "All Files (*)")
        if regular_results_file:
            self.regular_results_edit.setText(regular_results_file)

    def browse_csv_results(self):
        file_dialog = QFileDialog()
        csv_results_file, _ = file_dialog.getSaveFileName(self, "Select CSV Results File", "", "All Files (*)")
        if csv_results_file:
            self.csv_results_edit.setText(csv_results_file)

    def run_dnsmap(self):
        target = self.target_edit.text().strip()
        wordlist = self.wordlist_edit.text().strip()
        regular_results = self.regular_results_edit.text().strip()
        csv_results = self.csv_results_edit.text().strip()
        delay = self.delay_edit.text().strip()
        ips_ignore = self.ips_ignore_edit.text().strip()

        if not target:
            self.showMessageBox('Error', 'Please enter a target domain or IP.')
            return

        command = ['dnsmap', target]

        if wordlist:
            if os.path.isfile(wordlist):
                command.extend(['-w', wordlist])
            else:
                self.showMessageBox('Error', 'Wordlist file does not exist.')
                return

        if regular_results:
            command.extend(['-r', regular_results])

        if csv_results:
            command.extend(['-c', csv_results])

        if delay:
            try:
                delay = int(delay)
                if delay < 0:
                    raise ValueError
                command.extend(['-d', str(delay)])
            except ValueError:
                self.showMessageBox('Error', 'Delay must be a non-negative integer.')
                return

        if ips_ignore:
            command.extend(['-i', ips_ignore])

        try:
            self.output_display.append(f"Running dnsmap for {target}...\n")
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            self.output_display.append(output)
        except subprocess.CalledProcessError as e:
            self.output_display.append(f"Error: {e.output}")
        except Exception as ex:
            self.output_display.append(f"Error: {str(ex)}")

    def showMessageBox(self, title, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DnsmapGUI()
    sys.exit(app.exec_())
