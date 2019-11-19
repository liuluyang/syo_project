

print (__file__)
try:

    try:
        num = 1 + 'd'
    except Exception as e:
        print ('this is error:{}'.format(e))
        raise

except Exception as e:
    print ('out error:{}'.format(e))
