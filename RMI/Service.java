package SD;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Service extends Remote {
	
	// Interface do serviço oferecido
	public String echo(String entrada) throws RemoteException;

}