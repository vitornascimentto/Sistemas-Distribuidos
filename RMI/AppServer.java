package SD;

import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

public class AppServer {
	
    public static void main(String[] args) throws RemoteException {

        // Reservando uma porta local
        Registry registry =  LocateRegistry.createRegistry(5099);

        // atribuindo endereço do servico (CPF), e o servico (new ValidadorServico)
        registry.rebind("CPF", new Servant());

    }
}