# Teaching robots to cut food

We aim to empower robots with the ability to transform abstract knowledge from the web into actionable tasks, particularly in everyday manipulations like cutting, pouring or whisking.
By extracting information from diverse internet sources — ranging from biology textbooks and Wikipedia entries to cookbooks and instructional websites —, the robots create knowledge graphs that inform generalized action plans.
These plans enable robots to adapt cutting techniques such as slicing, quartering, and peeling to various fruits using suitable tools making abstract web knowledge practically applicable in robot perception-action loops.
More information on our approach and its application for teaching robots to cut fruits and vegetables can be found [here](https://vrb.ease-crc.org/explore-labs/knowledge-graph-lab/).

## Question-Answering on Robotic Food Cutting

To evaluate the task-specific commonsense capabilities of different state-of-the-art LLMs, we created a question-answering dataset from our food cutting ontology.
In each question, a concrete parameterization for a specific action or food object is asked. We provide the ground truth taken from the ontology in the dataset as well.
As an experimental evaluation, we query the following LLMs with these questions to assess how well their internal knowledge covers this task-specific commonsense knowledge.
For evaluating the correctness of their answer, we prompt an evaluator LLM (*Llama-3.3-70B-Instruct*) by providing the question, the answer given by the LLM and the ground truth.
We use two ways of classifying the results:
1) We ask for a binary classification whether the provided answer is correct and calculate the accuracy.
2) We ask it to quantify the results on a scale from 0 (= no answer is given) to 5 (= correct answer) and calculate the average score.

The results can be seen below:

| LLM                    | Correct Answers | Acc       | Avg. Score | Ans. w.o. score |
|------------------------|-----------------|-----------|------------|---------------|
| gemma-2-27b-it         | **139**         | **0.638** | 3.843      | 1             |
| gpt-4o-2024-08-06      | 121             | 0.555     | **4.028**  | 0             |
| Llama-3.3-70B-Instruct | 134             | 0.615     | 3.778      | 6             |

## Repository Structure
```bash
├── jupyter           # contains 2 jupyter notebooks for querying the onotlogy                           
├── owl               # contains the ontology as an .owl file
└── qa_d              # contains the question-answering dataset, the code to create and evaluate SOTA LLMs with it
```

## Publication

If you use the *Food Cutting* ontology or the resulting question-answering dataset, please cite the following paper:
```
@inproceedings{Kumpel2024KnowledgeEngineering,
  title = {Towards a Knowledge Engineering Methodology for Flexible Robot Manipulation in Everyday Tasks},
  booktitle = {ESWC 2024 Workshops and Tutorials Joint Proceedings},
  author = {K{\"u}mpel, Michaela and T{\"o}berg, Jan-Philipp and Hassouna, Vanessa and Cimiano, Philipp and Beetz, Michael},
  year = {2024},
  address = {Heraklion, Crete, Greece},
  url = {https://ceur-ws.org/Vol-3749/akr3-04.pdf},
}
```