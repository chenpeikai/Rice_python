'''my sultion'''

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    '''
    bulid the scoring matrix
    '''
    scoring_matrix = {'-':{'-':dash_score}}
    for char1 in alphabet:
        scoring_matrix['-'][char1] = dash_score
        scoring_matrix[char1] = {'-':dash_score}
        for char2 in alphabet:
            scoring_matrix[char1][char2] = (char1 == char2)*diag_score + (char1 != char2)*off_diag_score
    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag): 
    '''
    compute alignment matrix whose entry is the max socre of the 
    length of i,j
    '''
    width = len(seq_y) + 1
    height = len(seq_x) + 1
    alignment_matrix = [[0 for _ in range(width)] for _ in range(height)]
    for row in range(1,height):
        alignment_matrix[row][0] = scoring_matrix[seq_x[row-1]]['-'] + alignment_matrix[row-1][0]
        if global_flag == False and alignment_matrix[row][0] < 0:
            alignment_matrix[row][0] = 0
    for col in range(1,width):
        alignment_matrix[0][col] = scoring_matrix['-'][seq_y[col-1]] + alignment_matrix[0][col-1]
        if global_flag == False and alignment_matrix[0][col] < 0:
            alignment_matrix[0][col] = 0
    for row in range(1,height):
        for col in range(1,width):
            alignment_matrix[row][col] = max(alignment_matrix[row-1][col-1] + scoring_matrix[seq_x[row-1]][seq_y[col-1]],
            alignment_matrix[row-1][col] + scoring_matrix[seq_x[row-1]]['-'],
            alignment_matrix[row][col-1] + scoring_matrix['-'][seq_y[col-1]])
            if global_flag == False and alignment_matrix[row][col] < 0:
                alignment_matrix[row][col] = 0
    return alignment_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    compute the global alignment string for sqe_x and seq_y
    '''
    point_x = len(seq_x)
    point_y = len(seq_y)
    align_x = ''
    align_y = ''
    score = alignment_matrix[point_x][point_y]
    while point_x != 0 and point_y != 0:
        if alignment_matrix[point_x][point_y] == alignment_matrix[point_x-1][point_y-1] + scoring_matrix[seq_x[point_x-1]][seq_y[point_y-1]]:
            align_x = seq_x[point_x-1] + align_x
            align_y = seq_y[point_y-1] + align_y
            point_x -= 1
            point_y -= 1
        else:
            if alignment_matrix[point_x][point_y] == alignment_matrix[point_x-1][point_y] + scoring_matrix[seq_x[point_x-1]]['-']:
                align_x = seq_x[point_x-1] + align_x
                align_y = '-' + align_y
                point_x -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[point_y-1] + align_y
                point_y -= 1
    while point_x != 0:
        align_x = seq_x[point_x-1] + align_x
        align_y = '-' + align_y
        point_x -= 1
    while point_y != 0:
        align_x = '-' + align_x
        align_y = seq_y[point_y-1] + align_y
        point_y -= 1
    assert len(align_x) == len(align_y)
    return (score,align_x,align_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    ''''
    compute the local alignment string for sqe_x and seq_y
    '''
    align_x = ''
    align_y = ''
    max_entry = ()
    score = -float('inf')
    for row in range(len(alignment_matrix)):
        for col in range(len(alignment_matrix[0])):
            if alignment_matrix[row][col] > score:
                score = alignment_matrix[row][col]
                max_entry = (row,col)
    point_x = max_entry[0]
    point_y = max_entry[1]
    while point_x != 0 and point_y != 0:
        if alignment_matrix[point_x][point_y] == 0:
            break
        if alignment_matrix[point_x][point_y] == alignment_matrix[point_x-1][point_y-1] + scoring_matrix[seq_x[point_x-1]][seq_y[point_y-1]]:
            align_x = seq_x[point_x-1] + align_x
            align_y = seq_y[point_y-1] + align_y
            point_x -= 1
            point_y -= 1
        else:
            if alignment_matrix[point_x][point_y] == alignment_matrix[point_x-1][point_y] + scoring_matrix[seq_x[point_x-1]]['-']:
                align_x = seq_x[point_x-1] + align_x
                align_y = '-' + align_y
                point_x -= 1
            else:
                align_x = '-' + align_x
                align_y = seq_y[point_y-1] + align_y
                point_y -= 1
    return (score,align_x,align_y)

