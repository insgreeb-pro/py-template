docker build -t localhost:5000/ai-randomforest .
docker push localhost:5000/ai-randomforest 
docker build -t localhost:5000/ai-ann .
docker push localhost:5000/ai-ann 
docker build -t localhost:5000/ai-randomforest-ann .
docker push localhost:5000/ai-randomforest-ann 