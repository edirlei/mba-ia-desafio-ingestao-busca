from search import search_prompt

def main():
    print("Chat iniciado. Digite sua pergunta (Ctrl+C para sair).")

    while True:
        try:
            pergunta = input("\nPERGUNTA: ").strip()

            if not pergunta:
                continue

            resposta = search_prompt(pergunta)

            if not resposta:
                print("RESPOSTA: Não tenho informações necessárias para responder sua pergunta.")
            else:
                print(f"\nRESPOSTA: {resposta}")

        except KeyboardInterrupt:
            print("\nEncerrando chat.")
            break

if __name__ == "__main__":
    main()
