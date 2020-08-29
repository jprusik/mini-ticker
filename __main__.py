import ticker

def main():
    try:
        while True:
            ticker.update_display()
            ticker.time.sleep(60)

    except:
        ticker.shutdown()

main()
