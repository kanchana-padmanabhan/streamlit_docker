docker build -t dashboard_streamlit .
docker run -d -p 8501:8501 dashboard_streamlit
curl http://0.0.0.0:8501
