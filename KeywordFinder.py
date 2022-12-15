# imports
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity, pairwise_kernels, laplacian_kernel

# Part II: find keywords in pasted job description
# sample job description
text = """
Technologies & Tools We Use:
ML: PyTorch, DGL, NetworkX, XGboost, LightGBM, DVC, NVIDIA NeMo, HuggingFace, Weights & Biases
Deployment: Airflow, Docker, Kubernetes, AWS
Datastores: Postgres, Elasticsearch, SQLite, S3

What You’ll Do:
Conduct original research on large proprietary and open source data sets
Design, build and maintain scalable production-ready ML systems
Actively participate in the ML model lifecycle, from problem framing to training, deployment and monitoring in production
Partner with ML Operations team to deliver solutions for automating ML model lifecycle, from technical design to implementation
Work in a cross-functional team of ML engineers, Product Managers, Designers, Backend & Frontend engineers who are passionate about their product

What We Look For:
Outstanding people come from all different backgrounds, and we’re always interested in meeting talented people! Therefore, we do not require any particular credential or experience. If our work seems exciting to you, and you feel that you could excel in this position, we’d love to hear from you. That said, most successful candidates will fit the following profile, which reflects both our technical needs and team culture:

Bachelor's degree or higher with relevant classwork or internships in Machine Learning
Experience with advanced machine learning methods
Have strong statistical knowledge, intuition, and experience modeling real data
Have expertise in Python and Python-based ML frameworks (e.g., PyTorch or TensorFlow)
Demonstrated effective coding, documentation, and communication habits
Exercise strong communication skills and can effectively express even complicated methods and results to a broad, often non-technical audience
[optionally] Have published in top-tier journals and conferences in ML domain"""

human_keywords = ['pytorch', 'dgl', 'networkx', 'xgboost', 'lightgbm', 'dvc', 'nvidia', 'nemo', 'huggingface', 'weights', 'biases', 'airflow', 'docker', 'kubernetes',
                  'aws', 'postgres', 'elasticsearch', 'sqlite', 's3', 'research', 'ml', 'training', 'model', 'modeling', 'partner', 'bachelor', 'intern', 'data',
                  'python', 'pytorch', 'tensorflow', 'statistical', 'coding', 'documentation', 'communication', 'methods', 'machine', 'learning', 'published', 'journals',
                  'work', 'experience', 'design']

n_gram_range = (1, 1)
stop_words = "english"

# Extract candidate words/phrases
count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([text])
candidates = count.get_feature_names()

model = SentenceTransformer('distilbert-base-nli-mean-tokens')
doc_embedding = model.encode([text])
candidate_embeddings = model.encode(candidates)

top_n = 50

distances_cosine = cosine_similarity(doc_embedding, candidate_embeddings)
keywords_cosine = [candidates[index] for index in distances_cosine.argsort()[0][-top_n:]]

metrics = {'metric': ['linear', 'polynomial', 'rbf']}

distances_kernels = pairwise_kernels(doc_embedding, candidate_embeddings, metric='rbf')
keywords_kernels = [candidates[index] for index in distances_kernels.argsort()[0][-top_n:]]

distances_laplacian = laplacian_kernel(doc_embedding, candidate_embeddings)
keywords_laplacian = [candidates[index] for index in distances_laplacian.argsort()[0][-top_n:]]

cosine_likeness_score = len(list(set(human_keywords).intersection(keywords_cosine)))/len(human_keywords)
kernels_likeness_score = len(list(set(human_keywords).intersection(keywords_kernels)))/len(human_keywords)
laplacian_likeness_score = len(list(set(human_keywords).intersection(keywords_laplacian)))/len(human_keywords)

# percent of keywords in the human list of keywords that are generated
print("Cosine Similarity Score: ", cosine_likeness_score)
print("Pairwise Kernels (rbf) Score: ", kernels_likeness_score)
print("Laplacian Kernel Score: ", laplacian_likeness_score)

# pairwise kernels (rbf) does the best, so we will use this pairwise metric to find keywords from input job description
