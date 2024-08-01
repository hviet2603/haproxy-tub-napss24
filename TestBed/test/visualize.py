import requests
import re
import matplotlib.pyplot as plt
import math
import datetime

def _get_test_results():
    test_results = []
    res = requests.get('http://localhost:9090/api/v1/query?query=up')
    prometheus_up_queries = res.json()["data"]["result"]
    for elem in prometheus_up_queries:
        instance = elem["metric"]["instance"]
        if re.match(r"redis://cache_[0-9]+:6379", instance):
            label = instance.split("://")[1].split(":")[0]
            res = requests.get(f"http://localhost:9090/api/v1/query", params={ 'query': f'redis_keyspace_hits_total{{instance="{instance}"}}'})
            hits = int(res.json()["data"]["result"][0]["value"][1])
            res = requests.get(f"http://localhost:9090/api/v1/query", params={ 'query': f'redis_keyspace_misses_total{{instance="{instance}"}}'})
            misses = int(res.json()["data"]["result"][0]["value"][1])
            test_results.append({
                'order': int(label.split('_')[1]),
                'instance': instance,
                'label': label,
                'hits': hits,
                'misses': misses
            })
    
    test_results.sort(key=lambda result: result['order'])
            
    return test_results

def _visualize_test_results(data):
    labels = [item['label'] for item in data]
    hits = [item['hits'] for item in data]
    misses = [item['misses'] for item in data]

    # Calculate hits percentage for each label
    hits_percentage = [hit / (hit + miss) * 100 for hit, miss in zip(hits, misses)]

    # Calculate overall hits and misses
    total_hits = sum(hits)
    total_misses = sum(misses)
    overall_hits_rate = (total_hits / (total_hits + total_misses)) * 100

    # Calculate the average hits percentage
    average_hits_percentage = sum(hits_percentage) / len(hits_percentage)

    # Calculate variance and standard variance
    variance = sum([((hp - average_hits_percentage) ** 2) for hp in hits_percentage])/len(labels)
    std_deviation = math.sqrt(variance)
    
    # Create the bar chart
    plt.figure(figsize=(12, 8))
    bars = plt.bar(labels, hits_percentage, color='skyblue')

    # Annotate the value of each bar
    for bar, hp in zip(bars, hits_percentage):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() - 5,
                 f'{hp:.2f}%', ha='center', va='bottom', color='black')

    # Add the overall hits rate as a horizontal line
    plt.axhline(y=overall_hits_rate, color='red', linestyle='-', label=f'Overall Hits Rate: {overall_hits_rate:.2f}%')

    # Add the average hits percentage as a horizontal line
    plt.axhline(y=average_hits_percentage, color='green', linestyle='-', label=f'Average Hits Rate: {average_hits_percentage:.2f}%')

    # Plot the variance for each label's hits percentage as a line plot
    #plt.plot(labels, variance, color='orange', marker='o', label='Variance from Overall Rate')
    plt.axhline(y=std_deviation, color='blue', linestyle='-', label=f'Standard Deviation: {std_deviation:.2f}')

    # Add labels and title
    plt.xlabel('Cache Instances')
    plt.ylabel('Hits Rates (%)')
    plt.title('Cache Hits Percentage')
    plt.ylim(0, 100)
    plt.legend()

    #plt.show()
    plot_name = f"plot_{'_'.join(str(datetime.datetime.now()).split())}.png"
    plt.savefig(f"plots/{plot_name}")
    print(f"Plot saved at plots/{plot_name}.")

class TestVisualizer:
    def __init__(self):
        self.test_results = _get_test_results()
    
    def visualize(self):
        _visualize_test_results(self.test_results)


if __name__ == "__main__":
    v = TestVisualizer()
    v.visualize()