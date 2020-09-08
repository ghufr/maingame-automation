# Program untuk mengetahui tingkat okupansi bioskop
# Karena pandemi diantara setiap kursi diberi jarak 1 (kosong)
# Hitung okupansi jika kursi yang dikosongkan dihitung
# Hitung okupansi jika kursi yang dikosongkan tidak dihitung

SEATS = [{'A1', 'A3', 'A5'}, {'B1', 'B3', 'B5'}, {'C1', 'C3'}]

CUSTOMERS = [
    {
        'name': 'Gh',
        'tickets': ['A1', 'A3']
    },
    {
        'name': 'Fr',
        'tickets': ['B1', 'A1']
    }
]


def calc(occupancy):
    avail = 0
    empty = 0
    reserved = 0
    total = 0
    for row in occupancy:
        for col in row:
            total += 1
            if (col == 0):
                avail += 1
            elif (col == 1):
                reserved += 1
            else:
                empty += 1
    return avail, empty, reserved, total


def display(occupancy):
    print()
    print('=' * 22)
    avail, empty, reserved, total = calc(occupancy)
    print('Occupancy Rate: {}%'.format(round((reserved / avail) * 100)))
    print('Occupancy Rate Total: {}%'.format(
        round((reserved / total) * 100)))

    print()
    print('Total Seat:', total)
    print('Total Customer:', reserved, end='\n')
    print('Available Seat:', avail)
    print('Empty Seat (restricted):', empty)
    print('=' * 22, end='\n')


def main():
    occupancy = []
    total_avail_seat = 0
    # total_customer = 0
    # total_empty_seat = 0

    for seat in SEATS:
        num_of_seat = len(seat)

        temp = []
        for i in range(num_of_seat):
            if (i == num_of_seat - 1):
                temp.append(0)
                continue
            temp.append(0)
            temp.append(-1)
        occupancy.append(temp)
        total_avail_seat += num_of_seat
        # total_empty_seat += num_of_seat - 1

    display(occupancy)

    for customer in CUSTOMERS:
        tickets = customer['tickets']

        if (total_avail_seat - len(tickets) < 0):
            print('Bioskop sudah penuh')
            break

        for ticket in tickets:
            row_index = ord(ticket[0].lower()) - 97
            ticket_index = int(ticket[1])

            row_seat = SEATS[row_index]
            row_occupancy = occupancy[row_index]

            if (ticket in row_seat and row_occupancy[ticket_index - 1] == 0):
                occupancy[row_index][ticket_index - 1] = 1
                print('Kursi {} berhasil di pesan'.format(ticket))
                # total_customer += 1
                total_avail_seat -= 1
                # total_empty_seat -= 1
            else:
                print('Kursi {} tidak tersedia'.format(ticket))

    display(occupancy)


if __name__ == "__main__":
    main()
