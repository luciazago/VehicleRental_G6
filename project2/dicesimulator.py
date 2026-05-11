import random
import numpy as np

MIN_THROWS = 10
MAX_THROWS = 1000

def simulate(num_throws: int, num_dice: int):
    """
    Simulate rolling num_dice dice num_throws times.
    Returns a 2D numpy array of shape (num_throws, num_dice).
    """
    return np.random.randint(1, 7, size=(num_throws, num_dice))


def get_results(rolls):
    """suma los valores de los dados de cada tirada, si hay solo un dado también funciona (ese resultado mismio), el resultado es un array tambien."""
    return rolls.sum(axis=1)


def distribution(results):
    """cuenta cuántas veces aparece cada resultado, da los resultados en un diccionario"""
    values, counts = np.unique(results, return_counts=True)
    distribution_dict = {}

    for index in range(len(values)):
        value = int(values[index])
        count = int(counts[index])

        distribution_dict[value] = count

    return distribution_dict


def most_frequent(dist: dict) -> tuple:
    """busca el resultado que aparece más veces en el diccionario"""
    biggest_count = 0
    most_common_value = None

    for value in dist:

        if dist[value] > biggest_count:
            biggest_count = dist[value]
            most_common_value = value

    return most_common_value, biggest_count

def least_frequent(dist: dict):
    smallest_count = None
    least_common_value = None

    for value in dist:

        if smallest_count is None or dist[value] < smallest_count:
            smallest_count = dist[value]
            least_common_value = value

    return least_common_value, smallest_count

def empirical_probabilities(dist: dict, num_throws: int, num_dice: int):
    """
    Calculates empirical probability for each result, rounded to 4 decimals.
    For 1 die:  shows values 1-6  (missing ones get 0.0).
    For 2 dice: shows values 7-12 (missing ones get 0.0).
    """
    expected_range = range(1, 7) if num_dice == 1 else range(7, 13)
    return {v: round(dist.get(v, 0) / num_throws, 4) for v in expected_range}

def average(results: np.ndarray):
    return round(float(np.mean(results)), 4)


def minimum(results: np.ndarray):
    #Devuelve el valor minimo del array
    return int(np.min(results))


def maximum(results: np.ndarray):
    #Devuelve el valor maximo del array
    return int(np.max(results))

def evenness(results: np.ndarray, num_throws: int) -> dict:
    #Checks how evenly distributed the results are by looking at
    #the difference between the most and least frequent result
    #The smaller the difference, the more evenly distributed.

    dist = distribution(results)
    counts = [dist.get(v, 0) for v in range(1, 7)]
    max_diff = max(counts) - min(counts)
    threshold = max(1, int(len(results) / 6 * 0.1))
    verdict = "evenly distributed" if max_diff <= threshold else "not evenly distributed"
    return {"max_diff": max_diff, "verdict": verdict}


def doubles_percentage(rolls: np.ndarray):
    #calcula el porcentaje de dobles cuando lanzas 2 dados.
    #Only valid for 2 dice
    doubles = np.sum(rolls[:, 0] == rolls[:, 1])
    return round(float(doubles / len(rolls) * 100), 2)


def even_percentage(results: np.ndarray):
    return round(float(np.sum(results % 2 == 0) / len(results) * 100), 2)


def odd_percentage(results: np.ndarray):
    return round(float(np.sum(results % 2 != 0) / len(results) * 100), 2)


def run_analysis(num_throws: int, num_dice: int) -> dict:
    #Run the full simulation (aplica todas las funciones) and return all results in one dict.
    rolls = simulate(num_throws, num_dice)
    results = get_results(rolls)
    dist = distribution(results)
    num_throws_actual = len(results)

    most_v, most_c = most_frequent(dist)
    least_v, least_c = least_frequent(dist)

    analysis = {
        "rolls": rolls,
        "results": results,
        "num_throws": num_throws_actual,
        "num_dice": num_dice,
        "distribution": dist,
        "most_frequent": (most_v, most_c),
        "least_frequent": (least_v, least_c),
        "empirical_probabilities": empirical_probabilities(dist, num_throws_actual, num_dice),
        "average": average(results),
        "minimum": minimum(results),
        "maximum": maximum(results),
        "even_percentage": even_percentage(results),
        "odd_percentage": odd_percentage(results),
    }

    if num_dice == 1:
        analysis["evenness"] = evenness(results, num_throws_actual)

    if num_dice == 2:
        analysis["doubles_percentage"] = doubles_percentage(rolls)

    return analysis