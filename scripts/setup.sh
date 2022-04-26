mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"42744293+KonScanner@users.noreply.github.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = 8501\n\
" > ~/.streamlit/config.toml