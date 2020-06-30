def roc_auc_curve(X_test,y_test,model):
    """
    Plots the ROC AUC curve for a given model, x,y
    """
    
    ns_probs = [0 for _ in range(len(y_test))]
    
    # calculate scores
    ns_auc = roc_auc_score(y_test, ns_probs)
    lr_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
    
    
    # summarize scores
    print('RF: ROC AUC=%.3f' % (lr_auc))
    # calculate roc curves
    ns_fpr, ns_tpr, _ = roc_curve(y_test, ns_probs)
    lr_fpr, lr_tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:,1])
    # plot the roc curve for the model
    plt.figure(figsize = (8,8))
    plt.plot(ns_fpr, ns_tpr, linestyle='--',color='grey')
    plt.plot(lr_fpr, lr_tpr, marker='.')
    # axis labels
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate',rotation=0, labelpad=60)
    # title
    plt.title("ROC AUC CURVE")
    # show the plot
    plt.show()