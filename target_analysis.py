def target_analysis(df,target,var,xlim=[0,1000],n=50):

   

    if type(df) is DataFrame:

        df = df.select([var,target]).toPandas().apply(pd.to_numeric, downcast='float')

   

    n=n+1

   

    bins = np.linspace(xlim[0],xlim[1],n)

    df_grouped = df.groupby(pd.cut(df[var], bins))

  

    y_target_mean_all = df[target].mean()

    y_target_mean = df_grouped[target].mean().fillna(0)

    y_target_count = df_grouped[target].count().fillna(0)

    

    x = (bins [:-1] + bins [1:])/2

   

    plt.rcParams["figure.figsize"] = (10,5)

    fig, ax1 = plt.subplots()

   

    color = 'tab:blue'

    ax1.bar(x, y_target_count, color=color, width=(xlim[1]/n)*.75)

    ax1.set_xlabel(f'{var} values')

    ax1.set_ylabel('Number of cases',rotation=0, ha='right',va='center', ma='left')

   

    color = 'tab:orange'

    ax2 = ax1.twinx()

    ax2.plot(x, y_target_mean,color=color,label='Group target rate')

   

    color = 'tab:red'

    ax2.plot([xlim[0],xlim[1]], [y_target_mean_all,y_target_mean_all], 'r--', color=color, label='Dataset average target rate')

    ax2.set_ylabel('Target rate', rotation=0, ha='left',va='center', ma='right')

    ax2.set(xlim=(xlim[0], xlim[1]))

 

    fig.tight_layout() 

    plt.legend(loc='upper right')

   

    plt.show() 
