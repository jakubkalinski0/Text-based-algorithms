def naive_edit_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość edycyjną między dwoma ciągami używając naiwnego algorytmu rekurencyjnego.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość edycyjna (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    if not s1:
        return len(s2) 
    if not s2:
        return len(s1)  


    if s1[0] == s2[0]:
        return naive_edit_distance(s1[1:], s2[1:])

    delete_cost = 1 + naive_edit_distance(s1[1:], s2)      
    insert_cost = 1 + naive_edit_distance(s1, s2[1:])      
    replace_cost = 1 + naive_edit_distance(s1[1:], s2[1:]) 
    
    return min(delete_cost, insert_cost, replace_cost)

def naive_edit_distance_with_operations(s1: str, s2: str) -> tuple[int, list[str]]:
    """
    Oblicza odległość edycyjną i zwraca listę operacji potrzebnych do przekształcenia s1 w s2.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Krotka zawierająca odległość edycyjną i listę operacji
        Operacje: "INSERT x", "DELETE x", "REPLACE x->y", "MATCH x"
    """
    def _edit_distance_helper(s1, s2, i=0, j=0):
        if i == len(s1):
            operations = [f"INSERT {s2[k]}" for k in range(j, len(s2))]
            return len(s2) - j, operations
        if j == len(s2):
            operations = [f"DELETE {s1[k]}" for k in range(i, len(s1))]
            return len(s1) - i, operations

        if s1[i] == s2[j]:
            cost, operations = _edit_distance_helper(s1, s2, i+1, j+1)
            operations.insert(0, f"MATCH {s1[i]}")
            return cost, operations

        # Delete
        del_cost, del_ops = _edit_distance_helper(s1, s2, i+1, j)
        del_cost += 1
        del_ops.insert(0, f"DELETE {s1[i]}")

        # Insert
        ins_cost, ins_ops = _edit_distance_helper(s1, s2, i, j+1)
        ins_cost += 1
        ins_ops.insert(0, f"INSERT {s2[j]}")

        # Replace
        rep_cost, rep_ops = _edit_distance_helper(s1, s2, i+1, j+1)
        rep_cost += 1
        rep_ops.insert(0, f"REPLACE {s1[i]}->{s2[j]}")

        if del_cost <= ins_cost and del_cost <= rep_cost:
            return del_cost, del_ops
        elif ins_cost <= del_cost and ins_cost <= rep_cost:
            return ins_cost, ins_ops
        else:
            return rep_cost, rep_ops

    cost, operations = _edit_distance_helper(s1, s2)
    return cost, operations
