library("corrplot")
library("e1071")
library('mgcv')
library("reshape")
library("generalhoslem")



a<-read.csv(file="features_extraction.csv", header = TRUE, sep = ",")
a <- a[complete.cases(a),]
a
b<-cor(a[,2:13], method= "spearman")
cor(a[,2:13], method= "spearman")
corrplot(b)
corrplot(b, method = "number") 
corrplot(b,method="color",addCoef.col="grey") 
cor.test(a$num_url, a$count_word_title, alternative = "two.sided",method = "spearman",exact=FALSE, conf.level = 0.95)

model.final = glm(whether_solved_by_newcomers ~ log(num_url+1) + log(num_code+1) + log(num_comment+1) + log(num_table+1) + log(count_word_title+1) + 
                    log(count_word_body+1) + log(readability+23) + log(labeler_exper+1) + 
                    log(num_file+1) + log(num_add+1) +
                    log(num_delete+1) + log(stargazers_count+1),
                  data = a, 
                  family = binomial(link ="logit"), 
                  na.action(na.omit))

summary(model.final)
logitgof(a$whether_solved_by_newcomers, fitted(model.final))

model1 <- glm(whether_solved_by_newcomers ~ log(count_word_body+1) + log(num_delete+1) + 
                    log(labeler_exper+1)  + log(stargazers_count+1),
                  data = a, 
                  family = binomial(link ="logit"), 
                  na.action(na.omit))
summary(model)




