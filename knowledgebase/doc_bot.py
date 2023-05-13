import json, os, platform, faiss, langchain, openai
from urllib.parse import parse_qsl
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from gpt_index import GPTSimpleVectorIndex
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from .models import ChatHistory

from langchain.llms import OpenAI
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import DocumentationChatSerializer
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from gpt_index import SimpleDirectoryReader, GPTListIndex, readers, GPTSimpleVectorIndex, LLMPredictor, PromptHelper

os.environ['OPENAI_API_KEY'] = ""


class DocumentationViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentationChatSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def ask_lenny(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            query = request.data.get('query')
            try:
                chat_history_qs = ChatHistory.objects.filter(user=self.request.user.userprofile)
                chat_history = [(str(ch.question), str(ch.chat_history)) for ch in chat_history_qs]
            except:
                chat_history = []
            save_directory = "media/data/"
            embeddings = OpenAIEmbeddings()
            vectordb = FAISS.load_local(save_directory, embeddings)
            qa = ConversationalRetrievalChain.from_llm(llm = OpenAI(temperature = 0), retriever = vectordb.as_retriever())
            result = qa({"question": query, "chat_history" : chat_history})
            ChatHistory.objects.create(user=self.request.user.userprofile, question=query, chat_history=result["answer"])
            return Response({
                "answer" : result["answer"]
            }, status=200) 
        return Response({
            "error" : "went wrong"
        }, status=200) 
    
def file_and_conversation():
    try:
        file_url = "media/data/docs.pdf"
        save_directory = "faiss-data/"

        loader = UnstructuredPDFLoader(file_url)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)
        documents = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        vectordb = FAISS.from_documents(documents, embeddings)
        vectordb.save_local(save_directory)
        os.remove(file_url)
        return True
    except Exception as err:
        print(err)
        return False

def construct_index():
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_outputs = 256
    # set maximum chunk overlap
    max_chunk_overlap = 20
    # set chunk size limit
    chunk_size_limit = 600

    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003", max_tokens=num_outputs))
    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
 
    documents = SimpleDirectoryReader("data").load_data()
    index = GPTSimpleVectorIndex(
        documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
    )

    index.save_to_disk('index.json')

    return index