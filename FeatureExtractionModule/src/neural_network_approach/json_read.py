import json
import pandas as pd

# outputs average accuracy values through epochs. Read from .json file
# TODO: modify to detect between different problems .json files (classification or regression)


def __main__():
    idents = ['2gu87', 'iz2ps', '1mpau', '7dwjy', '7swyk', '94mnx', 'bd47a', 'c24ur', 'ctsax', 'dkhty', 'e4gay',
              'ef5rq', 'f1gjp', 'hpbxa', 'pmyfl', 'r89k1', 'tn4vl', 'td5pr', 'gyqu9', 'fzchw', 'l53hg', '3n2f9',
              '62i9y']

    # idents = ['7dwjy', 'bd47a', 'f1gjp', 'hpbxa', 'l53hg', 'tn4vl']
    # idents = ['94mnx', 'fzchw', 'ef5rq', 'iz2ps', 'c24ur', 'td5pr', '3n2f9', 'r89k1']

    with open('compl2_2_GC_kernel_100_pool_4_filter_64_strides_4_lstm_256.json', 'r') as f:
        datastore = json.load(f)

    val_acc_epoch = pd.DataFrame()  # accuracy through epochs
    val_loss_epoch = pd.DataFrame()
    for ident in idents:
        val_acc_epoch[ident] = datastore[ident]['val_acc']  # valtidation accuracy
        # val_acc_epoch[ident] = datastore[ident]['val_mean_absolute_error']  # or MAE, if regression problem
        val_loss_epoch[ident] = datastore[ident]['val_loss']

    print('Values (accuracy) through epochs: \n', val_acc_epoch.mean(axis=1).to_string(), '\n')
    print('Loss function value through epochs: \n', val_loss_epoch.mean(axis=1).to_string(), '\n')


__main__()
