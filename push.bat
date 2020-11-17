docker build -t mwafa/ai-randomforest .
docker tag mwafa/ai-randomforest localhost:5000/ai-randomforest
docker push localhost:5000/ai-randomforest 