import sys
from PyQt5.QtGui import QDoubleValidator, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget, QFrame, QTabWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import FuncFormatter


def custom_round(value):
    rounded_value = round(value)
    return float(f"{rounded_value}.00")

class LoanCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.initUI()

    def initUI(self):
        self.setWindowTitle("╨Ü╤Ç╨╡╨┤╨╕╤é╨╡╨╜ ╨Ü╨░╨╗╨║╤â╨╗╨░╤é╨╛╤Ç")
        self.setFixedSize(700, 800)

        self.tabs = QTabWidget()

        self.tab1 = QWidget()
        self.init_tab1()
        self.tabs.addTab(self.tab1, "╨Ü╨░╨╗╨║╤â╨╗╨░╤é╨╛╤Ç")

        self.tab2 = QWidget()
        self.init_tab2()
        self.tabs.addTab(self.tab2, "╨ô╤Ç╨░╤ä╨╕╨║╨╛╨╜╨╕")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def init_tab1(self):
        tab1_layout = QVBoxLayout()

        disclaimer_label = QLabel(
            "<b>╨Æ╨░╨╢╨╜╨╛:</b> ╨ƒ╤Ç╨╡╤ü╨╝╨╡╤é╨║╨░╤é╨░ ╨▓╨░╨╢╨╕ ╨╖╨░ ╨╖╨░╨╡╨╝ ╤ü╨║╨╗╤â╤ç╨╡╨╜ ╨▓╨╛ ╨░╨╜╤â╨╕╤é╨╡╤é╨╕ ╤ü╨╛ ╤ä╨╕╨║╤ü╨╜╨░ ╨║╨░╨╝╨░╤é╨╜╨░ ╤ü╤é╨░╨┐╨║╨░. ╨£╨╛╨╢╨╡ ╨┤╨░ ╨╕╨╝╨░ ╨╖╨░╨╜╨╡╨╝╨░╤Ç╨╗╨╕╨▓╨╕ ╤Ç╨░╨╖╨╗╨╕╨║╨╕ ╨▓╨╛ ╤ü╨┐╨╛╤Ç╨╡╨┤╨▒╨░ ╤ü╨╛ ╤ä╨░╨║╤é╨╕╤ç╨║╨░╤é╨░ ╨┐╤Ç╨╡╤ü╨╝╨╡╤é╨║╨░ ╨║╨░╤ÿ ╨┐╨╛╨╡╨┤╨╕╨╜╨╡╤ç╨╜╨╕ ╨▒╨░╨╜╨║╨╕, ╨▓╨╛ ╨╖╨░╨▓╨╕╤ü╨╜╨╛╤ü╤é ╨╛╨┤ ╨╝╨╡╤é╨╛╨┤╨╕╤é╨╡ ╨╖╨░ ╨┐╤Ç╨╡╤ü╨╝╨╡╤é╨║╨░ ╨╜╨░ ╨║╨░╨╝╨░╤é╨░╤é╨░. ╨ª╨╡╨╗╤é╨░ ╨╜╨░ ╨┐╤Ç╨╡╤ü╨╝╨╡╤é╨║╨░╤é╨░ ╨╡ ╨┤╨░ ╤ü╨╡ ╨╛╨▓╨╛╨╖╨╝╨╛╨╢╨╕ ╨╕ ╨┤╨░ ╤ü╨╡ ╨┤╨╛╤ÿ╨┤╨╡ ╨┤╨╛ ╨╖╨░╨║╨╗╤â╤ç╨╛╨║ ╨╖╨░ ╨┐╤Ç╨╛╤ä╨╕╤é╨░╨▒╨╕╨╗╨╜╨╛╤ü╤é╨░ ╨╜╨░ ╨╡╨┤╨╜╨╛╨║╤Ç╨░╤é╨╜╨░╤é╨░ ╨╛╤é╨┐╨╗╨░╤é╨░ ╨╜╨░ ╨╖╨░╨╡╨╝╨╛╤é. <br /><i>╨Æ╨╜╨╡╤ü╨╡╤é╨╡ ╨│╨╕ ╨▓╨░╤ê╨╕╤é╨╡ ╨║╤Ç╨╡╨┤╨╕╤é╨╜╨╕ ╨╕╨╜╤ä╨╛╤Ç╨╝╨░╤å╨╕╨╕ ╨╖╨░ ╨┤╨░ ╤ÿ╨░ ╨┤╨╛╨▒╨╕╨╡╤é╨╡ ╨▓╨░╤ê╨░╤é╨░ ╨┐╤Ç╨╡╤ü╨╝╨╡╤é╨║╨░.</i>"
        )
        disclaimer_label.setWordWrap(True)
        tab1_layout.addWidget(disclaimer_label)

        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.Box)
        input_frame.setFrameShadow(QFrame.Raised)
        input_layout = QGridLayout()

        self.loan_amount_input = self.create_input_field("╨ÿ╨╖╨╜╨╛╤ü ╨╜╨░ ╨║╤Ç╨╡╨┤╨╕╤é╨╛╤é (Γé¼):")
        self.interest_rate_input = self.create_input_field("╨ô╨╛╨┤╨╕╤ê╨╜╨░ ╨║╨░╨╝╨░╤é╨╜╨░ ╤ü╤é╨░╨┐╨║╨░ (%):")
        self.total_installments_input = self.create_input_field("╨Æ╨║╤â╨┐╨╡╨╜ ╨▒╤Ç╨╛╤ÿ ╨╜╨░ ╨░╨╜╤â╨╕╤é╨╡╤é╨╕ (╤é╤Ç╨░╨╡╤Ü╨╡ ╨╜╨░ ╨║╤Ç╨╡╨┤╨╕╤é╨╛╤é * 12):")
        self.paid_installments_input = self.create_input_field("╨₧╤é╨┐╨╗╨░╤é╨╡╨╜╨╕ ╨░╨╜╤â╨╕╤é╨╡╤é╨╕ (╨╝╨╡╤ü╨╡╤å╨╕):")

        input_layout.addWidget(QLabel("╨Ü╤Ç╨╡╨┤╨╕╤é╨╜╨╕ ╨╕╨╜╤ä╨╛╤Ç╨╝╨░╤å╨╕╨╕"), 0, 0, 1, 2)
        input_layout.addWidget(self.loan_amount_input[0], 1, 0)
        input_layout.addWidget(self.loan_amount_input[1], 1, 1)
        input_layout.addWidget(self.interest_rate_input[0], 2, 0)
        input_layout.addWidget(self.interest_rate_input[1], 2, 1)
        input_layout.addWidget(self.total_installments_input[0], 3, 0)
        input_layout.addWidget(self.total_installments_input[1], 3, 1)
        input_layout.addWidget(self.paid_installments_input[0], 4, 0)
        input_layout.addWidget(self.paid_installments_input[1], 4, 1)

        button_layout = QVBoxLayout()
        self.calculate_button = QPushButton("╨ƒ╤Ç╨╡╤ü╨╝╨╡╤é╨░╤ÿ")
        self.calculate_button.clicked.connect(self.calculate)
        self.reset_button = QPushButton("╨á╨╡╤ü╨╡╤é╨╕╤Ç╨░╤ÿ")
        self.reset_button.clicked.connect(self.reset)
        button_layout.addWidget(self.calculate_button)
        button_layout.addWidget(self.reset_button)
        input_layout.addLayout(button_layout, 1, 2, 4, 1)

        input_frame.setLayout(input_layout)
        tab1_layout.addWidget(input_frame)

        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.Box)
        result_frame.setFrameShadow(QFrame.Raised)
        result_layout = QVBoxLayout()

        self.result_label = QLabel("╨ƒ╨╛╨┤╨░╤é╨╛╤å╨╕╤é╨╡ ╨╖╨░ ╨║╨░╨╝╨░╤é╨╕╤é╨╡ ╨╕ ╨│╨╗╨░╨▓╨╜╨╕╤å╨╕╤é╨╡ ╤ü╨╡ ╨┐╤Ç╨╡╤ü╨╝╨╡╤é╤â╨▓╨░╨░╤é ╨░╨▓╤é╨╛╨╝╨░╤é╤ü╨║╨╕")
        self.result_label.setWordWrap(True)
        self.result_label.setFont(QFont("Arial", 11))
        result_layout.addWidget(self.result_label)

        result_frame.setLayout(result_layout)
        tab1_layout.addWidget(result_frame)

        self.additional_frame = QFrame()
        self.additional_frame.setFrameShape(QFrame.Box)
        self.additional_frame.setFrameShadow(QFrame.Raised)
        self.additional_frame.setVisible(False)  # Hide by default

        additional_layout = QVBoxLayout()
        self.additional_label = QLabel("")
        self.additional_label.setWordWrap(True)
        self.additional_label.setFont(QFont("Arial", 14))
        additional_layout.addWidget(self.additional_label)
        self.additional_frame.setLayout(additional_layout)
        tab1_layout.addWidget(self.additional_frame)

        self.tab1.setLayout(tab1_layout)

    def init_tab2(self):
        tab2_layout = QVBoxLayout()

        self.chart_canvas_1 = FigureCanvas(Figure(figsize=(5, 3)))
        self.chart_canvas_2 = FigureCanvas(Figure(figsize=(5, 3)))
        self.chart_canvas_3 = FigureCanvas(Figure(figsize=(5, 3)))

        tab2_layout.addWidget(self.chart_canvas_1)
        tab2_layout.addWidget(self.chart_canvas_2)
        tab2_layout.addWidget(self.chart_canvas_3)

        self.tab2.setLayout(tab2_layout)

    def create_input_field(self, label_text):
        label = QLabel(label_text)
        input_field = QLineEdit()
        input_field.setValidator(QDoubleValidator())
        input_field.setFixedWidth(150)
        return label, input_field

    def cumulative_interest(self, rate, nper, pv, start_period, end_period):
        """
        Calculate cumulative interest paid between start_period and end_period,
        matching Excel's CUMIPMT behavior with intermediate rounding.
        """
        interest = 0
        balance = pv
        monthly_payment = round(balance * (rate * (1 + rate) ** nper) / ((1 + rate) ** nper - 1), 2)

        for period in range(1, nper + 1):
            current_interest = round(balance * rate, 2)

            if start_period <= period <= end_period:
                interest += current_interest

            principal_payment = round(monthly_payment - current_interest, 2)
            balance -= principal_payment

            balance = max(balance, 0)

        return round(interest, 2)

    def format_number(self, value):
        """Format numbers for display."""
        return "{:,.2f}".format(value)

    def calculate(self):
        try:
            P = float(self.loan_amount_input[1].text())
            r = float(self.interest_rate_input[1].text()) / 100 / 12
            n = int(self.total_installments_input[1].text())
            paid = int(self.paid_installments_input[1].text())

            if P <= 0 or r <= 0 or n <= 0 or paid < 0 or paid > n:
                raise ValueError("╨Æ╨╜╨╡╤ü╨╡╨╜╨╕╤é╨╡ ╨┐╨╛╨┤╨░╤é╨╛╤å╨╕ ╨╜╨╡ ╤ü╨╡ ╤é╨╛╤ç╨╜╨╕.")

            monthly_payment = round(P * (r * (1 + r) ** n) / ((1 + r) ** n - 1), 2)

            total_interest = round(monthly_payment * n - P, 2)

            total_paid = round(monthly_payment * paid, 2)

            paid_principal = round(P * ((1 + r) ** paid - 1) / ((1 + r) ** n - 1), 2)

            interest_paid = round(total_paid - paid_principal, 2)

            remaining_principal = round(P - paid_principal, 2)

            remaining_interest = self.cumulative_interest(r, n, P, paid + 1, n)

            principal_percentage_paid = round((paid_principal / P) * 100, 2)

            interest_percentage_paid = round((interest_paid / total_interest) * 100, 2)

            if remaining_principal > 0 and n > paid:
                break_even_rate = (((remaining_principal + remaining_interest) / remaining_principal) **
                                   (12 / (n - paid)) - 1) * 100
            else:
                break_even_rate = 0

            self.result_label.setText(
                f"<b>╨ƒ╨╛╨┤╨░╤é╨╛╤å╨╕ ╨╖╨░ ╨║╨░╨╝╨░╤é╨╕ ╨╕ ╨│╨╗╨░╨▓╨╜╨╕╤å╨░:</b><br>"
                f"╨£╨╡╤ü╨╡╤ç╨╡╨╜ ╨░╨╜╤â╨╕╤é╨╡╤é: {self.format_number(monthly_payment)} Γé¼<br>"
                f"╨₧╤é╨┐╨╗╨░╤é╨╡╨╜╨░ ╨│╨╗╨░╨▓╨╜╨╕╤å╨░: {self.format_number(paid_principal)} Γé¼<br>"
                f"╨ƒ╤Ç╨╡╨╛╤ü╤é╨░╨╜╨░╤é╨░ ╨│╨╗╨░╨▓╨╜╨╕╤å╨░: {self.format_number(remaining_principal)} Γé¼<br>"
                f"<b>╨Ü╨╛╨╗╨║╤â ╤ü╤é╨╡ ╨╕╤ü╨┐╨╗╨░╤é╨╕╨╗╨╡ ╨╛╨┤ ╨│╨╗╨░╨▓╨╜╨╕╤å╨░╤é╨░:</b> {principal_percentage_paid:.2f} %<br>"
                f"╨Æ╨║╤â╨┐╨╜╨░ ╨║╨░╨╝╨░╤é╨░: {self.format_number(total_interest)} Γé¼<br>"
                f"╨₧╤é╨┐╨╗╨░╤é╨╡╨╜╨░ ╨║╨░╨╝╨░╤é╨░: {self.format_number(interest_paid)} Γé¼<br>"
                f"╨ƒ╤Ç╨╡╨╛╤ü╤é╨░╨╜╨░╤é╨░ ╨║╨░╨╝╨░╤é╨░: {self.format_number(remaining_interest)} Γé¼<br>"
                f"<b>╨Ü╨╛╨╗╨║╤â ╤ü╤é╨╡ ╨┐╨╗╨░╤é╨╕╨╗╨╡ ╨╛╨┤ ╨║╨░╨╝╨░╤é╨░╤é╨░:</b> {interest_percentage_paid:.2f} %<br>"
                f"╨ô╨╛╨┤╨╕╤ê╨╜╨░╤é╨░ ╨║╨░╨╝╨░╤é╨╜╨░ ╤ü╤é╨░╨┐╨║╨░ ╤ê╤é╨╛ ╤ÿ╨░ ╨┐╨╗╨░╤£╨░╤é╨╡ ╨┤╨╛ ╨║╤Ç╨░╤ÿ╨╛╤é ╨╜╨░ ╨┐╤Ç╨╡╤ü╨╝╨╡╤é╨║╨░╤é╨░ ╨╖╨░ ╨╛╤é╨┐╨╗╨░╤é╨░ ╨╜╨░ ╨║╤Ç╨╡╨┤╨╕╤é╨╛╤é. Break-even: {break_even_rate:.2f}%"
            )

            self.additional_label.setText(
                f"╨₧╨┤ ╨┐╨╛╤ç╨╡╤é╨╜╨╕╨╛╤é ╨╕╨╖╨╜╨╛╤ü ╨╜╨░ ╨│╨╗╨░╨▓╨╜╨╕╤å╨░╤é╨░ ╨╛╨┤ {self.format_number(P)} ╨╡╨▓╤Ç╨░, ╨┤╨╛ ╤ü╨╡╨│╨░ ╤ü╤é╨╡ ╨╛╤é╨┐╨╗╨░╤é╨╕╨╗╨╡ {self.format_number(paid_principal)} ╨╡╨▓╤Ç╨░, ╨╕╨╗╨╕ {(paid_principal / P) * 100:.2f}%. "
                f"╨₧╨┤ ╨▓╨║╤â╨┐╨╜╨░╤é╨░ ╨║╨░╨╝╨░╤é╨░ ╨║╨╛╤ÿ╨░ ╨╕╨╖╨╜╨╡╤ü╤â╨▓╨░ {self.format_number(total_interest)} ╨╡╨▓╤Ç╨░, ╨┤╨╛ ╤ü╨╡╨│╨░ ╤ü╤é╨╡ ╨╛╤é╨┐╨╗╨░╤é╨╕╨╗╨╡ {self.format_number(interest_paid)} ╨╡╨▓╤Ç╨░, ╨╕╨╗╨╕ {interest_percentage_paid:.2f}%. "
                f"╨í╨┐╨╛╤Ç╨╡╨┤ ╨╛╨▓╨╕╨╡ ╨┐╨╛╨┤╨░╤é╨╛╤å╨╕ ╨║╨░╨╝╨░╤é╨╜╨░╤é╨░ ╤ü╤é╨░╨┐╨║╨░ ╨┤╨╛ ╨╖╨░╨▓╤Ç╤ê╤â╨▓╨░╤Ü╨╡╤é╨╛ ╨╜╨░ ╤Ç╨╛╨║╨╛╤é ╨╖╨░ ╨╛╤é╨┐╨╗╨░╤é╨░ ╨╜╨░ ╨║╤Ç╨╡╨┤╨╕╤é╨╛╤é ╨╕╨╖╨╜╨╡╤ü╤â╨▓╨░ {self.format_number(break_even_rate)}%. "
                f"╨¿╤é╨╛ ╨╖╨╜╨░╤ç╨╕ ╨┤╨╡╨║╨░ ╨░╨║╨╛ ╨╝╨╛╨╢╨╡╤é╨╡ ╤ü╨╛ ╨╕╨╜╨▓╨╡╤ü╤é╨╕╤Ç╨░╤Ü╨╡ ╨┤╨░ ╨╛╤ü╤é╨▓╨░╤Ç╨╕╤é╨╡ ╨┐╨╛╨│╨╛╨╗╨╡╨╝ ╨┐╨╛╨▓╤Ç╨░╤é ╨╛╨┤ {self.format_number(break_even_rate)}%, ╤é╨╛╨│╨░╤ê ╨╜╨╡ ╨▓╨╕ ╤ü╨╡ ╨╕╤ü╨┐╨╗╨░╤é╨╕ ╨┤╨░ ╨│╨╛ ╨╖╨░╤é╨▓╨░╤Ç╨░╤é╨╡ ╨║╤Ç╨╡╨┤╨╕╤é╨╛╤é ╨┐╤Ç╨╡╨┤╨▓╤Ç╨╡╨╝╨╡╨╜╨╛."
            )
            self.additional_frame.show()

            self.plot_charts(P, n, paid, monthly_payment, paid_principal, remaining_principal, total_interest,
                             interest_paid, remaining_interest)

        except ValueError:
            self.result_label.setText("╨Æ╨╜╨╡╤ü╨╡╤é╨╡ ╨▓╨░╨╗╨╕╨┤╨╜╨╕ ╨┐╨╛╨┤╨░╤é╨╛╤å╨╕.")
            self.additional_frame.hide()

    def reset(self):
        self.loan_amount_input[1].setText("")
        self.interest_rate_input[1].setText("")
        self.total_installments_input[1].setText("")
        self.paid_installments_input[1].setText("")
        self.result_label.setText("╨ƒ╨╛╨┤╨░╤é╨╛╤å╨╕╤é╨╡ ╨╖╨░ ╨║╨░╨╝╨░╤é╨╕╤é╨╡ ╨╕ ╨│╨╗╨░╨▓╨╜╨╕╤å╨╕╤é╨╡ ╤ü╨╡ ╨┐╤Ç╨╡╤ü╨╝╨╡╤é╤â╨▓╨░╨░╤é ╨░╨▓╤é╨╛╨╝╨░╤é╤ü╨║╨╕")
        self.additional_label.setText("")
        self.additional_frame.hide()
        self.chart_canvas_1.figure.clear()
        self.chart_canvas_2.figure.clear()
        self.chart_canvas_3.figure.clear()
        self.chart_canvas_1.figure.canvas.draw()
        self.chart_canvas_2.figure.canvas.draw()
        self.chart_canvas_3.figure.canvas.draw()

    def format_number(self, value):
        return f"{value:,.2f}"

    def plot_charts(self, loan_amount, total_installments, paid_installments, monthly_payment, paid_principal,
                    remaining_principal, total_interest, interest_paid, remaining_interest):

        self.plot_total_loan_chart(
            self.chart_canvas_1.figure, loan_amount, monthly_payment * total_installments
        )

        self.plot_principal_chart(
            self.chart_canvas_2.figure,
            loan_amount,
            paid_principal,
            remaining_principal
        )

        self.plot_interest_chart(
            self.chart_canvas_3.figure,
            total_interest,
            interest_paid,
            remaining_interest
        )

    def plot_total_loan_chart(self, fig, loan_amount, total_payment):
        fig.clear()
        ax = fig.add_subplot(111)
        categories = ["╨ÿ╨╖╨╜╨╛╤ü ╨╜╨░ ╨║╤Ç╨╡╨┤╨╕╤é", "╨Æ╨║╤â╨┐╨╜╨╛ ╨▓╤Ç╨░╤£╨░╤é╨╡"]
        values = [loan_amount, total_payment]
        colors = ["#7f8c8d", "#c0392b"]

        bars = ax.bar(categories, values, color=colors, width=0.3)

        for bar, value in zip(bars, values):
            rounded_value = custom_round(value)
            ax.text(bar.get_x() + bar.get_width() / 2, rounded_value + 200,
                    f"{rounded_value:,.2f} Γé¼", ha="center", va="bottom", fontsize=10)

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{custom_round(x):,.2f} Γé¼"))
        ax.set_ylim(0, ((custom_round(max(values)) // 100) + 1) * 100 * 1.2)

        ax.set_title("╨Æ╨║╤â╨┐╨╡╨╜ ╨Ü╤Ç╨╡╨┤╨╕╤é", fontsize=13, fontweight="bold")
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()
        fig.canvas.draw()

    def plot_principal_chart(self, fig, loan_amount, paid_principal, remaining_principal):
        """Plot the Principal chart."""
        fig.clear()
        ax = fig.add_subplot(111)
        categories = ["╨Æ╨║╤â╨┐╨╜╨░ ╨│╨╗╨░╨▓╨╜╨╕╤å╨░", "╨₧╤é╨┐╨╗╨░╤é╨╡╨╜╨░ ╨│╨╗╨░╨▓╨╜╨╕╤å╨░", "╨ƒ╤Ç╨╡╨╛╤ü╤é╨░╨╜╨░╤é╨░ ╨│╨╗╨░╨▓╨╜╨╕╤å╨░"]
        values = [loan_amount, paid_principal, remaining_principal]
        colors = ["#7f8c8d", "#a3b1b2", "#c0392b"]

        bars = ax.bar(categories, values, color=colors, width=0.3)

        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.05 * max(values),
                    f"{value:,.2f} Γé¼", ha="center", va="bottom", fontsize=10)

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{custom_round(x):,.2f} Γé¼"))
        ax.set_ylim(0, ((max(values) // 100) + 1) * 100 * 1.2)
        ax.set_title("╨ô╨╗╨░╨▓╨╜╨╕╤å╨░", fontsize=13, fontweight="bold")
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()
        fig.canvas.draw()

    def plot_interest_chart(self, fig, total_interest, interest_paid, remaining_interest):
        """Plot the Interest chart."""
        fig.clear()
        ax = fig.add_subplot(111)
        categories = ["╨Æ╨║╤â╨┐╨╜╨░ ╨║╨░╨╝╨░╤é╨░", "╨₧╤é╨┐╨╗╨░╤é╨╡╨╜╨░ ╨║╨░╨╝╨░╤é╨░", "╨ƒ╤Ç╨╡╨╛╤ü╤é╨░╨╜╨░╤é╨░ ╨║╨░╨╝╨░╤é╨░"]
        values = [total_interest, interest_paid, remaining_interest]
        colors = ["#7f8c8d", "#a3b1b2", "#c0392b"]

        bars = ax.bar(categories, values, color=colors, width=0.3)

        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, custom_round(value), f"{custom_round(value):,.2f} Γé¼",
                    ha="center", va="bottom")

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{custom_round(x):,.2f} Γé¼"))
        ax.set_ylim(0, ((max(values) // 100) + 1) * 100 * 1.2)
        ax.set_title("╨Ü╨░╨╝╨░╤é╨░", fontsize=13, fontweight="bold")
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()
        fig.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoanCalculatorApp()
    window.show()
    sys.exit(app.exec_())
