import logging, sys, argparse


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_entity(tag_seq, char_seq):
    ENT = get_ENT_entity(tag_seq, char_seq)
    HYPER = get_HYPER_entity(tag_seq, char_seq)
    # ORG = get_ORG_entity(tag_seq, char_seq)
    return ENT, HYPER


def get_ENT_entity(tag_seq, char_seq):
    length = len(char_seq)
    ENT = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-ENT':
            if 'ent' in locals().keys():
                ENT.append(ent)
                del ent
            ent = char
            if i+1 == length:
                ENT.append(ent)
        if tag == 'I-ENT':
            ent += char
            if i+1 == length:
                ENT.append(ent)
        if tag not in ['B-ENT', 'I-ENT']:
            if 'ent' in locals().keys():
                ENT.append(ent)
                del ent
            continue
    return ENT


def get_HYPER_entity(tag_seq, char_seq):
    length = len(char_seq)
    HYPER = []
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-HYPER':
            if 'hyper' in locals().keys():
                HYPER.append(hyper)
                del hyper
            hyper = char
            if i+1 == length:
                HYPER.append(hyper)
        if tag == 'I-HYPER':
            hyper += char
            if i+1 == length:
                HYPER.append(hyper)
        if tag not in ['B-HYPER', 'I-HYPER']:
            if 'hyper' in locals().keys():
                HYPER.append(hyper)
                del hyper
            continue
    return HYPER


def get_logger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger