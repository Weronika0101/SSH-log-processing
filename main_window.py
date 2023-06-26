
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from log_processing import logFilter,getDetails,getLogsFromFile

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowTitle("Logi")
        
        #listy logów
        self.logListWidget = QListWidget()
        self.logListWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.logListWidget.itemSelectionChanged.connect(self.showLogDetails)
        
        #szczegóły loga
        self.logDetailsGroupBox = QGroupBox("Szczegóły loga")
        self.logDetailsLayout = QFormLayout()
        self.hostLabel = QLabel()
        self.dateLabel = QLabel()
        self.timeLabel = QLabel()
        self.PIDLabel = QLabel()
        self.ipLabel = QLabel()

        self.logDetailsLayout.addRow("Host:", self.hostLabel)
        self.logDetailsLayout.addRow("Data:", self.dateLabel)
        self.logDetailsLayout.addRow("Czas:", self.timeLabel)
        self.logDetailsLayout.addRow("PID:", self.PIDLabel)
        self.logDetailsLayout.addRow("Adres IP:", self.ipLabel)

        self.logDetailsGroupBox.setLayout(self.logDetailsLayout)
        
        #wczytywanie logów z pliku
        self.loadLogsButton = QPushButton("Wczytaj logi")
        self.loadLogsButton.setStyleSheet("background-color : #72c0d4")
        self.chooseFile = QLineEdit()
        self.label = QLabel()
        self.chooseFile.textChanged.connect(self.chooseFile.setText)
        
        self.loadLogsButton.clicked.connect(self.loadLogs)
        
        #filtrowanie logów po dacie
        self.fromDateEdit = QDateEdit(QDate.currentDate())
        self.toDateEdit = QDateEdit(QDate.currentDate())
        self.filterLogsButton = QPushButton("Filtruj")
        self.fromDateEdit.setCalendarPopup(True)
        self.toDateEdit.setCalendarPopup(True)
        self.filterLogsButton.clicked.connect(self.filterLogs)
        
        #nawigacja
        self.prevLogButton = QPushButton("Poprzedni")
        self.prevLogButton.setEnabled(False)
        self.prevLogButton.clicked.connect(self.prevLog)
        self.nextLogButton = QPushButton("Następny")
        self.nextLogButton.setEnabled(False)
        self.nextLogButton.clicked.connect(self.nextLog)
        

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.loadLogsButton)
        topLayout.addWidget(self.chooseFile)
        topLayout.addWidget(self.label)
        mainLayout = QVBoxLayout()
        
        mainLayout.addWidget(self.logListWidget)
        mainLayout.addWidget(self.logDetailsGroupBox)
        
        buttonLayout = QHBoxLayout()
        
        buttonLayout.addWidget(QLabel("Od:"))
        buttonLayout.addWidget(self.fromDateEdit)
        buttonLayout.addWidget(QLabel("Do:"))
        buttonLayout.addWidget(self.toDateEdit)
        buttonLayout.addWidget(self.filterLogsButton)
        buttonLayout.addWidget(self.prevLogButton)
        buttonLayout.addWidget(self.nextLogButton)
        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(buttonLayout)

        
        self.setLayout(mainLayout)
        
        # Inicjalizacja danych logów
        self.logs = []
        self.current_log_index = -1
        self.filteredlogs = []


    def showLogDetails(self):
        self.updateDetails()
        currRow = self.logListWidget.currentItem()
        
        result = getDetails(currRow)

        self.dateLabel.setText(result[0])
        self.timeLabel.setText(result[1])
        self.hostLabel.setText(result[2])
        self.PIDLabel.setText(result[3])
        self.ipLabel.setText(result[4])



    def loadLogs(self):
        self.logListWidget.clear()
        file_name = self.chooseFile.text()
        try:
            log_list = getLogsFromFile(file_name)
  
            for line in log_list:           
                item = QListWidgetItem(line)
                self.logListWidget.addItem(item)
        except FileNotFoundError:
            self.showWarning()
        self.logs=log_list
        

    def filterLogs(self):
        filtered_logs = logFilter(self.fromDateEdit.date().toPython(),self.toDateEdit.date().toPython(),self.logListWidget)
        if filtered_logs is not -1:
            self.logListWidget.clear()
            for log in filtered_logs:
                item = QListWidgetItem(log)
                self.logListWidget.addItem(item)
        else:
            self.showWarningDate()

    def updateDetails(self):
                     
            index = self.logListWidget.currentIndex().row()
            self.current_log_index = index
            length = self.logListWidget.count()
            if index == 0:
                self.prevLogButton.setEnabled(False)
            else:
                self.prevLogButton.setEnabled(True)

            if index == length -1 :
                self.nextLogButton.setEnabled(False)
            else:
                self.nextLogButton.setEnabled(True)


    def nextLog(self):
            self.logListWidget.setCurrentRow(self.current_log_index + 1)
            self.current_log_index += 1
            self.updateDetails()


    def prevLog(self):
        if self.current_log_index > 0:
            self.logListWidget.setCurrentRow(self.current_log_index - 1)
            self.current_log_index -= 1
            self.updateDetails()


    def showWarning(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning!")
        dlg.setText("Taki plik nie istnieje!")
        button = dlg.exec_()

        if button == QMessageBox.Ok:
            print("OK")

    def showWarningDate(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Warning!")
        dlg.setText("Wpisano niepoprawne daty!")
        button = dlg.exec_()

        if button == QMessageBox.Ok:
            print("OK")