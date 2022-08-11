if (T){
  #library(readxl)   
  library(lme4) 		  #mixed models
  library(lmerTest) 	#mixed models p values
  library(sjPlot)
  library(ggplot2) 	   #graphs
  #library(GGally) 	   #ggpairs
  #library(car) 		   #corelations
  #library(reshape2)
  #library(pastecs)   #descriptives
}
setwd("~/sciebo/GuiltAndResponsibility/")
socialchoicedata <- read.csv('Smith and Krajbich - 2018 - Attention and choice across domains/osfstorage-archive/socialchoicedata.csv')

#### Read data ----
attach(socialchoicedata)

#arranging data
socialchoicedata$MeLeft     <- ifelse(socialchoicedata$TopRowPayoffs =="Me", socialchoicedata$ValueUpLeft,socialchoicedata$ValueLowerLeft)
socialchoicedata$MeRight    <- ifelse(socialchoicedata$TopRowPayoffs =="Me", socialchoicedata$ValueUpRight,socialchoicedata$ValueLowerRight)

socialchoicedata$OtherLeft  <- ifelse(socialchoicedata$TopRowPayoffs =="You", socialchoicedata$ValueUpLeft,socialchoicedata$ValueLowerLeft)
socialchoicedata$OtherRight <- ifelse(socialchoicedata$TopRowPayoffs =="You", socialchoicedata$ValueUpRight,socialchoicedata$ValueLowerRight)

#calculate differences for self and other
socialchoicedata$Z_diff_self         <- scale(socialchoicedata$MeLeft - socialchoicedata$MeRight, center=T)
socialchoicedata$Z_diff_other        <- scale(socialchoicedata$OtherLeft - socialchoicedata$OtherRight, center=T)
socialchoicedata$diff_self           <- socialchoicedata$MeLeft - socialchoicedata$MeRight
socialchoicedata$diff_other          <- socialchoicedata$OtherLeft - socialchoicedata$OtherRight


#factor choice variable 
socialchoicedata$ChoseRight <- socialchoicedata$LeftRight-1
socialchoicedata$ChoseLeft  <- as.factor(ifelse(socialchoicedata$ChoseRight=="1",0,1))
class(socialchoicedata$ChoseLeft)

#### 1. Mixed-logistic regression ----
#otherwise known as a generalized linear model
model1 <-glmer(ChoseLeft ~ Z_diff_self + Z_diff_other+(1|SubjectNumber), family = binomial(link = "logit"), data = socialchoicedata)
summary(model1)
tab_model(model1)
#plot_model(model1, type = "pred", terms = c("Z_diff_self[all]", "Z_diff_other[all]"), data = socialchoicedata)
#package called sjPlot
self  <- plot_model(model1, type = "pred", terms = c("Z_diff_self[all]"), data = socialchoicedata)
other <- plot_model(model1, type = "pred", terms = c("Z_diff_other[all]"), data = socialchoicedata)
library(gridExtra)
grid.arrange(self, other, ncol = 2)

#another way to graph the results
#package ggeffects
library(ggeffects)
self <- ggpredict(model1, terms= "Z_diff_self[all]", ci.lvl = 0.95)
plot(self)

other <- ggpredict(model1, terms = "Z_diff_other[all]")
plot(other)

##to plot them together
a <- rbind(self, other)
a$type <- c(rep(c("self"),times = length(self$predicted)), rep(c("other"), times= length(other$predicted)))
ggplot(a, aes(a$x, a$predicted, color = a$type)) + geom_point() + geom_line()+ geom_ribbon(aes(ymin = a$conf.low, ymax = a$conf.high, alpha = 0.85))


#### 2. Single-subject estimates ----
#estimate a logistic model for every participant separately
Subjects  =  split(socialchoicedata,socialchoicedata$SubjectNumber)                # splits the data so that we have the data of each subject as separated , split by a criteria
results   =  lapply(Subjects, function(socialchoicedata) glm(ChoseLeft ~diff_self+diff_other, family=binomial(link="logit"), data=socialchoicedata))

lapply(results, coefficients) #to get the coefficients 
lapply(results, summary)      #to get all results
lapply(results, Anova)        #to get the effect 

Estimates                 <- as.data.frame(cbind(t(as.data.frame (lapply(results, coefficients))), sort(unique(socialchoicedata$SubjectNumber))))
colnames(Estimates)       <- c("Intercept","Self difference", "Other difference", "Subject_ID")

#graph it 
plot_data <- data.frame(c(Estimates$`Self difference`, Estimates$`Other difference`),
                           c(rep(c("diff_self", "diff_other"), each = 36)),
                           c(Estimates$Subject_ID, Estimates$Subject_ID))

colnames(plot_data) <- c("Estimate","Type","Subject_ID")

library(plotly)
ggplotly(ggplot(plot_data,aes(x = Type, y = plot_data$Estimate, 
                              col = factor(plot_data$Subject_ID)))+
           geom_jitter()+ scale_y_continuous(breaks =seq(-2,13,0.5)))
ggsave("/Graphs/Single subject estimates.pdf", dpi = 300, width= 25, height = 20, units = "cm")
ggsave("Single subject estimates.pdf", dpi = 300)

t.test(Estimates$`Self difference`,Estimates$`Other difference`, paired = T)

#density plots
plot(density(plot_data$Estimate[plot_data$Type=="diff_self"]))
plot(density(plot_data$Estimate[plot_data$Type=="diff_other"]))

##some useful commands
help("ggsave")
??ggsave
help.start()




