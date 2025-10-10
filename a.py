def reverse(string):
    return string[::-1]

def getMinEditDistance(source, target):
    rows = len(source) + 1
    cols = len(target) + 1
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    # Initialization
    for i in range(rows):
        matrix[i][0] = i
    for j in range(cols):
        matrix[0][j] = j

    # Fill DP
    for i in range(1, rows):
        for j in range(1, cols):
            if source[i-1] == target[j-1]:
                cost = 0
            else:
                cost = 2   # mismatch penalty

            matrix[i][j] = min(
                matrix[i-1][j] + 1,      # deletion
                matrix[i][j-1] + 1,      # insertion
                matrix[i-1][j-1] + cost  # match/mismatch
            )

    # Print result
    print("Source: " + source)
    print("Target: " + target)
    print("-----")
    print("Distance: ", matrix[len(source)][len(target)])
    print("Alignment:")

    # Backtracing
    t_alignment, s_alignment, operations = "", "", ""
    i, j = len(source), len(target)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and source[i-1] == target[j-1] and matrix[i][j] == matrix[i-1][j-1]:
            t_alignment += source[i-1]
            s_alignment += target[j-1]
            operations += " "
            i, j = i-1, j-1

        elif i > 0 and j > 0 and matrix[i][j] == matrix[i-1][j-1] + 2:
            t_alignment += source[i-1]
            s_alignment += target[j-1]
            operations += "M"
            i, j = i-1, j-1

        elif j > 0 and matrix[i][j] == matrix[i][j-1] + 1:
            t_alignment += "-"
            s_alignment += target[j-1]
            operations += "I"
            j = j-1

        elif i > 0 and matrix[i][j] == matrix[i-1][j] + 1:
            t_alignment += source[i-1]
            s_alignment += "-"
            operations += "D"
            i = i-1

    print(reverse(t_alignment))
    print(reverse(operations))
    print(reverse(s_alignment))
    print()


getMinEditDistance("kitten", "sitting")
getMinEditDistance("flaw", "lawn")
getMinEditDistance("intention", "execution")



def getMinEditDistanceDL(source, target):
    rows = len(source) + 1
    cols = len(target) + 1
    matrix = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(rows):
        matrix[i][0] = i
    for j in range(cols):
        matrix[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            if source[i-1] == target[j-1]:
                cost = 0
            else:
                cost = 1  # substitution cost

            matrix[i][j] = min(
                matrix[i-1][j] + 1,      # deletion
                matrix[i][j-1] + 1,      # insertion
                matrix[i-1][j-1] + cost  # substitution/match
            )

            # Bonus: transposition
            if i > 1 and j > 1 and source[i-1] == target[j-2] and source[i-2] == target[j-1]:
                matrix[i][j] = min(matrix[i][j], matrix[i-2][j-2] + 1)

    print("Source: " + source)
    print("Target: " + target)
    print("-----")
    print("Distance: ", matrix[len(source)][len(target)])
    print("Note: This version has Damerau-Levenshtein rules (S=1, T=1)")
    print()

getMinEditDistanceDL("abcd", "acbd")
