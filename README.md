# CRUtility

Choosing between two lotteries which gives payoff to self and inaddition to another player.
===
Notations:
Left: Left lottery
Right: Right lottery


28/06/22:

Checking the decision made based on the difference of the payoffs in the two lotteries.
- Set up data, auhtors changed the position where the payoffs were displyed, made it consistent
- Set up two boxplots to see the likelihood of the choices between Left and Right. Choice is on x axis and difference in me payoff and other payoff is on the y axis.
- Made two plots. One shows choice vs difference for Left, second for Right.

Observations
- When Left gives me very less than other then I tend to reject it more often.
- When Left gives more than other by a large margin (>100) tendency to accept decreases.
- But there is a greater tendency to reject Left when the difference is even a little negative (ie other gets more then even 0).
- So participants not so keen on accepting higher offers but keen on rejecting lower offers.

Accept "fair" offers (b/w 0 to 100), reject "unfair" offers (below 0). Why not accept higher offers with greater likelihood? Maybe it gives more to the other player? (Envy?) (Check!). Or maybe it is guilt? (Proposal: if the payoffs of the other player was high too and the offer was rejected then it was probably envy, if the payoff of the other player was small then it was probably the guilt of accepting a high offer at the expense of another which drove the decision)


29/06/22:


1/7/22:
- So, instead of using x1 and (x2-x1), use just (x2-x1) in Gridsearchcv? (since there is only one parameter, x1 goes into the error term: look up assumptions of logistic regression)
- Try different solver for LogisticRegression? (is MLE relevant? idea is to implement mle through solver) (https://towardsdatascience.com/dont-sweat-the-solver-stuff-aea7cddc3451)
- probability density (frequency of occurance in the ...)
