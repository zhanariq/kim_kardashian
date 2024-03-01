import PyPDF2, re
from collections import defaultdict

if __name__ == '__main__':

    # Replace with your actual file name
    file_path = 'storage/kaspi_1m.pdf'

    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        stats = defaultdict(int)
        total = 0
        for i, page in enumerate(pdf_reader.pages):
            text = page.extract_text()

            print(f"Page {i + 1}:")
            for j, line in enumerate(text.split('\n')):
                if not line:
                    continue
                if i == 0 and j < 15:
                    continue
                elif i != 0 and j == 0 or (i == len(pdf_reader.pages)-1 and j == len(text.split('\n'))-2):
                    continue
                line = re.sub(r'\s+', ' ', line)
                line = re.sub(r'(\d) +(\d)', r'\1\2', line)
                data = line.split(' ')
                if len(data) < 5:
                    continue
                sign, amount, recipient = data[1], float(data[2].replace(',', '.')), data[-2]+data[-1]
                # we aren't interested in replenishments
                if sign == '+':
                    continue
                # don't want to include deposit
                if recipient != 'KaspiDeposit':
                    total += amount
                stats[recipient] += amount

                print(line, data)
    print(total)

    print(sorted(stats.items(), key=lambda x: -x[1]))
