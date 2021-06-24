from django.shortcuts import redirect, render
from .models import Document
from .forms import DocumentForm
import sys
import os
import sys
import pickle
import math
from collections import Counter
from subprocess import run,PIPE
from retrievalmodel.utils import textprocessing, helpers
def home(request):
	return render(request,'home.html')

def output(request):
	data = 'Nowadays, with the huge amount of information made available on the internet, individuals continuously capture data some which are beneficial to them and some which are not.  More so, the realization of making information available to users almost instantly is already a blessing since information plays a vital role in everyday activities such as for writing reports, preparing plans and making decisions, e.t.c.  However, without better methods to filter and retrieve relevant information from this unlimited influx of information, users face information overload.'
	return render(request, 'process.html',{'data':data})

def external(request):
	text = request.POST.get('uname')
	out = run([sys.executable,'C://Users//chukwunenyea//Desktop//NLK_for_chibuike//retrievalmodel//query.py',text],shell=False,stdout=PIPE)
	out = str(out.stdout)
	out = out.split('\\n')
	return render(request, 'process.html',{'data':out})
	
def upload(request):
    message = 'Upload a file!'
    model= 'name'
    fields= ["name"]

    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('upload')
        else:
            message = 'The form is not valid'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all
    # Render list page with the documents and the form
    out = indexer()
    context = {'documents': documents, 'form': form, 'message': message, 'out': out}
    return render(request, 'list.html', context)

def indexer():
    resultant= []
    resultant.append('Indexing....')

    resources_path = os.path.join(os.getcwd(), 'retrievalmodel//resources')
    data_path = os.path.join(os.getcwd(), 'retrievalmodel//data')

    if not os.path.isdir(resources_path):
        resultant.append('ERROR: The {} is not a directory or does not exist'.format(
            resources_path))

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    # Get dataset path and stopwords file
    dataset_path = os.path.join(resources_path, 'dataset')
    stopwords_file = os.path.join(resources_path, 'stopwords_en.txt')

    # Get stopwords set
    stopwords = helpers.get_stopwords(stopwords_file)

    docs = helpers.get_docs(dataset_path)
    corpus = []
    for doc in docs:
        with open(doc, mode='r') as f:
            text = f.read()
            words = textprocessing.preprocess_text(text, stopwords)
            bag_of_words = Counter(words)
            corpus.append(bag_of_words)

    idf = helpers.compute_idf(corpus)
    for doc in corpus:
        helpers.compute_weights(idf, doc)
        helpers.normalize(doc)

    inverted_index = helpers.build_inverted_index(idf, corpus)

    docs_file = os.path.join(data_path, 'docs.pickle')
    inverted_index_file = os.path.join(data_path, 'inverted_index.pickle')
    dictionary_file = os.path.join(data_path, 'dictionary.txt')

    # Serialize data
    with open(docs_file, 'wb') as f:
        pickle.dump(docs, f)

    with open(inverted_index_file, 'wb') as f:
        pickle.dump(inverted_index, f)

    with open(dictionary_file, 'w') as f:
        for word in idf.keys():
            f.write(word + '\n')
    resultant.append('Index done.')

    return resultant
    
def precisionrecall():
    result =[]
    totalFiles = 0
    docsFolder = os.path.join(resources_path, 'dataset')

    for base, dirs, files in os.walk(docsFolder):
        result.append('Searcing files')

        for Files in files:
            totalFiles += 1

