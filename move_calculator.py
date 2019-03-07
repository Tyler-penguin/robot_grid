import os

def initializations(filename):
    with open(filename, 'r') as f:
        current_line = f.readline()
        str_pos = current_line.split(',')
        pos = [int(str_pos[0].strip()), int(str_pos[1].strip())]
        moves = int(f.readline())

        matrix = []
        for line in f:
            seperated_line = line.split(',')
            row = []
            for val_string in seperated_line:
                row.append(int(val_string.strip()))
            matrix.append(row)

        rowlen = len(matrix)
        collen = len(matrix[0])

        padded_matrix = []
        padded_matrix.append([None for i in range(collen+2)])
        for row in range(rowlen):
            padded_matrix.append([None])
            for num in matrix[row]:
                padded_matrix[row+1].append(num)
            padded_matrix[row+1].append(None)
        padded_matrix.append([None for i in range(collen+2)])
    return pos, 50, padded_matrix

def write_to_file(move_list):
    my_dir = os.path.dirname(os.path.realpath(__file__))
    with open(my_dir + '/' + 'robot.moves', 'w') as f:
        f.write('row, col\n')
        for move in move_list:
            f.write(f'{move[0]}, {move[1]}\n')

def recursive_step(pos, moves, matrix, total, max, move_list, max_move_list, end_pos):
    if moves == 0:
        if total > max:
            max = total
            max_move_list = move_list
            end_pos = pos
        return max, max_move_list, end_pos
    for row in range(-1, 2):
        for col in range(-1, 2):
            if (row!=0 or col!=0):
                new_pos = [pos[0]+row, pos[1]+col]
                try:
                    spot_value = matrix[new_pos[0]][new_pos[1]]
                    matrix[new_pos[0]][new_pos[1]] = 0
                    new_total = total+spot_value
                    new_move_list = move_list + [[row, col]]
                    max, max_move_list, end_pos= recursive_step(new_pos, moves-1, matrix, new_total, max, new_move_list, max_move_list, end_pos)
                    matrix[new_pos[0]][new_pos[1]] = spot_value
                except:
                    pass

    return max, max_move_list, end_pos

def mark_zeros(matrix, pos, moves):
    matrix[pos[0]][pos[1]] = 0
    for movement in moves:
        pos[0] += movement[0]
        pos[1] += movement[1]
        matrix[pos[0]][pos[1]] = 0
    return matrix

def find_moves(filename):
    pos, moves, matrix = initializations(filename)
    pos[0] +=1
    pos[1] +=1
    chunk_size = 6
    if moves > 50:
        chunk_size = 5
        if moves > 300:
            chunk_size = 4
            if moves > 2250:
                chunk_size = 3
    move_list = []
    spot_value = matrix[pos[0]][pos[1]]
    matrix[pos[0]][pos[1]]=0
    max = 0
    for i in range(moves//chunk_size):
        maxes = recursive_step(pos, chunk_size, matrix, spot_value, 0, [], [], pos)

        max+=maxes[0]
        matrix = mark_zeros(matrix, pos, maxes[1])
        pos = maxes[2]
        move_list += maxes[1]
    # print(maxes)
    [new_max, move_order, _] = recursive_step(pos, moves%chunk_size, matrix, spot_value, 0, [], [], pos)
    max+=new_max
    move_list += move_order
    write_to_file(move_list)


my_dir = os.path.dirname(os.path.realpath(__file__))
filename = 'robot.map.100x100.csv'
filename = my_dir + '/' + filename
## Be careful as the BigO is 9^x ##
find_moves(filename)
