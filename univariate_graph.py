#!/usr/bin/env python

def univariate_graph(data, var, **kwargs):
    '''
    This function takes at least a dataset and a variable name of the dataset. The variable name should be the feature you are looking at.
    It then groups by the variable values and calculates the amount of observations in the variable's categories and the percentage of 
    defaults in each category. If your variable is not categorical, it takes on an extra argument, n_bins, to make it categorical.
    The outcome of the variable is a plot that shows the amount of observations in each bucket as bars and the share of defaults as a line.
    '''
    df = data.copy()
    if type(df[var][0]) == str:
        df = df.groupby(var).agg({
            'TARGET' : [np.mean, len], 
            })
    else:
        df[var] = KBinsDiscretizer(**kwargs, 
                                   encode = 'ordinal',
                                   strategy = 'uniform',
                                  ).fit_transform(df[[var]])
        df = df.groupby(var).agg({
            'TARGET' : [np.mean, len],
            })
        
#     make graph
    fig, ax1 = plt.subplots()
    ax1.set_title(var.replace('_', ' '))
#     bar plot
    ax1.tick_params(axis = 'x', 
                    rotation = 45,
                   )
    ax1.set_ylabel('Anzahl', 
                   color = 'blue',
                  )
    ax1.bar(list(df.index),
            list(df['TARGET']['len']),
            label = 'Anzahl',
            color = 'blue',
            )
    ax1.tick_params(axis = 'y', 
                    labelcolor = 'blue',
                   ) 
#     line graph
    ax2 = ax1.twinx() 
    ax2.set_ylabel('Ausfallquote', 
                   color = 'red',
                   ) 
    ax2.plot(df['TARGET']['mean'],
             label = 'Ausfallquote', 
             color = 'red',
             ) 
    ax2.tick_params(axis = 'y', 
                    labelcolor = 'red') 
#     save figure
    plt.savefig(var+'.png')
#     show plot
    plt.show() 


if __name__ == '__main__':
    univariate_graph(X_train, 'NAME_EDUCATION_TYPE')