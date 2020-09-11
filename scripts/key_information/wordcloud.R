library(wordcloud)
library(tm) 
library(slam)

fileName0<-"keywords_body_type0.txt"
SC0<-readChar(fileName0, nchars=999999)

nchar(SC0)

fileName1<-"keywords_body_type1.txt"
SC1<-readChar(fileName1, nchars=999999)
wordVC <- c(SC0, SC1)
corpus <- (VectorSource(wordVC))
corpus <- VCorpus(corpus)
corpus
summary(corpus)
tdm <- TermDocumentMatrix(corpus)
ma <- as.matrix(tdm)
ma
colnames(ma) <- c("Other Issues","Good First Issues")
comparison.cloud(ma, max.words = 40, scale = c(3,0.8), random.order=FALSE, rot.per=.0,
                 colors = c("red","#339900"), title.colors=c("red","#339900"), title.size = 1.5)

comparison.cloud(ma, max.words = 30, scale = c(3,0.8), random.order=FALSE, rot.per=.0,
                 colors = c("red","#339900"), title.size = 1)



