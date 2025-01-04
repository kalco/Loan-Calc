import sys, os
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
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        icon_path = os.path.join(base_path, "icon.ico")

        self.setWindowIcon(QIcon(icon_path))
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Кредитен Калкулатор")
        self.setFixedSize(700, 800)

        self.tabs = QTabWidget()

        self.tab1 = QWidget()
        self.init_tab1()
        self.tabs.addTab(self.tab1, "Калкулатор")

        self.tab2 = QWidget()
        self.init_tab2()
        self.tabs.addTab(self.tab2, "Графикони")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def init_tab1(self):
        tab1_layout = QVBoxLayout()

        disclaimer_label = QLabel(
        "<b>Важно:</b> Пресметката важи за заем склучен во ануитети со фиксна каматна стапка. Може да има занемарливи разлики во споредба со фактичката пресметка кај поединечни банки, во зависност од методите за пресметка на каматата. Целта на пресметката е да се овозможи и да се дојде до заклучок за профитабилноста на еднократната отплата на заемот. <br /><i>Внесете ги вашите кредитни информации за да ја добиете вашата пресметка.</i>")
        disclaimer_label.setWordWrap(True)
        tab1_layout.addWidget(disclaimer_label)

        input_frame = QFrame()
        input_frame.setFrameShape(QFrame.Box)
        input_frame.setFrameShadow(QFrame.Raised)
        input_layout = QGridLayout()

        self.loan_amount_input = self.create_input_field("Износ на кредитот (€):")
        self.interest_rate_input = self.create_input_field("Годишна каматна стапка (%):")
        self.total_installments_input = self.create_input_field("Вкупен број на ануитети (траење на кредитот * 12):")
        self.paid_installments_input = self.create_input_field("Отплатени ануитети (месеци):")

        input_layout.addWidget(QLabel("Кредитни информации"), 0, 0, 1, 2)
        input_layout.addWidget(self.loan_amount_input[0], 1, 0)
        input_layout.addWidget(self.loan_amount_input[1], 1, 1)
        input_layout.addWidget(self.interest_rate_input[0], 2, 0)
        input_layout.addWidget(self.interest_rate_input[1], 2, 1)
        input_layout.addWidget(self.total_installments_input[0], 3, 0)
        input_layout.addWidget(self.total_installments_input[1], 3, 1)
        input_layout.addWidget(self.paid_installments_input[0], 4, 0)
        input_layout.addWidget(self.paid_installments_input[1], 4, 1)

        button_layout = QVBoxLayout()
        self.calculate_button = QPushButton("Пресметај")
        self.calculate_button.clicked.connect(self.calculate)
        self.reset_button = QPushButton("Ресетирај")
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

        self.result_label = QLabel("Податоците за каматите и главниците се пресметуваат автоматски")
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
                raise ValueError("Внесените податоци не се точни.")

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
                f"<b>Податоци за камати и главница:</b><br>"
                f"Месечен ануитет: {self.format_number(monthly_payment)} €<br>"
                f"Отплатена главница: {self.format_number(paid_principal)} €<br>"
                f"Преостаната главница: {self.format_number(remaining_principal)} €<br>"
                f"<b>Колку сте исплатиле од главницата:</b> {principal_percentage_paid:.2f} %<br>"
                f"Вкупна камата: {self.format_number(total_interest)} €<br>"
                f"Отплатена камата: {self.format_number(interest_paid)} €<br>"
                f"Преостаната камата: {self.format_number(remaining_interest)} €<br>"
                f"<b>Колку сте платиле од каматата:</b> {interest_percentage_paid:.2f} %<br>"
                f"Годишната каматна стапка што ја плаќате до крајот на пресметката за отплата на кредитот. Break-even: {break_even_rate:.2f}%"
            )

            self.additional_label.setText(
                f"Од почетниот износ на главницата од {self.format_number(P)} евра, до сега сте отплатиле {self.format_number(paid_principal)} евра, или {(paid_principal / P) * 100:.2f}%. "
                f"Од вкупната камата која изнесува {self.format_number(total_interest)} евра, до сега сте отплатиле {self.format_number(interest_paid)} евра, или {interest_percentage_paid:.2f}%. "
                f"Според овие податоци каматната стапка до завршувањето на рокот за отплата на кредитот изнесува {self.format_number(break_even_rate)}%. "
                f"Што значи дека ако можете со инвестирање да остварите поголем поврат од {self.format_number(break_even_rate)}%, тогаш не ви се исплати да го затварате кредитот предвремено."
            )
            self.additional_frame.show()

            self.plot_charts(P, n, paid, monthly_payment, paid_principal, remaining_principal, total_interest,
                             interest_paid, remaining_interest)

        except ValueError:
            self.result_label.setText("Внесете валидни податоци.")
            self.additional_frame.hide()

    def reset(self):
        self.loan_amount_input[1].setText("")
        self.interest_rate_input[1].setText("")
        self.total_installments_input[1].setText("")
        self.paid_installments_input[1].setText("")
        self.result_label.setText("Податоците за каматите и главниците се пресметуваат автоматски")
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
        categories = ["Износ на кредит", "Вкупно враќате"]
        values = [loan_amount, total_payment]
        colors = ["#7f8c8d", "#c0392b"]

        bars = ax.bar(categories, values, color=colors, width=0.3)

        for bar, value in zip(bars, values):
            rounded_value = custom_round(value)
            ax.text(bar.get_x() + bar.get_width() / 2, rounded_value + 200,
                    f"{rounded_value:,.2f} €", ha="center", va="bottom", fontsize=10)

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{custom_round(x):,.2f} €"))
        ax.set_ylim(0, ((custom_round(max(values)) // 100) + 1) * 100 * 1.2)

        ax.set_title("Вкупен Кредит", fontsize=13, fontweight="bold")
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()
        fig.canvas.draw()

    def plot_principal_chart(self, fig, loan_amount, paid_principal, remaining_principal):
        """Plot the Principal chart."""
        fig.clear()
        ax = fig.add_subplot(111)
        categories = ["Вкупна главница", "Отплатена главница", "Преостаната главница"]
        values = [loan_amount, paid_principal, remaining_principal]
        colors = ["#7f8c8d", "#a3b1b2", "#c0392b"]

        bars = ax.bar(categories, values, color=colors, width=0.3)

        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, value + 0.05 * max(values),
                    f"{value:,.2f} €", ha="center", va="bottom", fontsize=10)

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{custom_round(x):,.2f} €"))
        ax.set_ylim(0, ((max(values) // 100) + 1) * 100 * 1.2)
        ax.set_title("Главница", fontsize=13, fontweight="bold")
        ax.grid(False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()
        fig.canvas.draw()

    def plot_interest_chart(self, fig, total_interest, interest_paid, remaining_interest):
        """Plot the Interest chart."""
        fig.clear()
        ax = fig.add_subplot(111)
        categories = ["Вкупна камата", "Отплатена камата", "Преостаната камата"]
        values = [total_interest, interest_paid, remaining_interest]
        colors = ["#7f8c8d", "#a3b1b2", "#c0392b"]

        bars = ax.bar(categories, values, color=colors, width=0.3)

        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, custom_round(value), f"{custom_round(value):,.2f} €",
                    ha="center", va="bottom")

        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{custom_round(x):,.2f} €"))
        ax.set_ylim(0, ((max(values) // 100) + 1) * 100 * 1.2)
        ax.set_title("Камата", fontsize=13, fontweight="bold")
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
