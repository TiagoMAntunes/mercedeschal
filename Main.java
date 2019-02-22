import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.TimeUnit;
import jdk.nashorn.internal.parser.JSONParser; //verificar como usar

public class Main {

    public static void main(String[] args) {
        String input;
        BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));

        try {
            System.out.print("> ");
            while (!(input = bf.readLine()).equals("exit")) {
                String[] tokens = input.split(" ");
                if (tokens.length == 0)
                    continue;

                switch (tokens[0]) {
                case "poll":
                    for (Service v : Service.values())
                        System.out.println("[" + v + "] " + v.isOnline());
                    break;
                case "fetch":
                    int time;
                    try {
                        time = Integer.parseInt(tokens[1]);
                    } catch (IndexOutOfBoundsException e) {
                        time = 5;
                    }
                    while (true) {
                        for (Service v : Service.values())
                            System.out.println("[" + v + "] " + v.isOnline());

                        try {
                            TimeUnit.SECONDS.sleep(time);
                        } catch (InterruptedException e) {
                            e.printStackTrace();
                        }
                    }
                case "history":
                    for (Service v : Service.values())
                        for (String s : v.getHistory())
                            System.out.println("[" + v + "] " + s);
                    break;
                case "backup":
                case "restore":
                case "services":
                case "help":
                case "status":
                    System.out.println("Command: " + tokens[0]);
                    break;
                default:
                    System.out.println("Invalid command");
                }
                System.out.print("> ");
            }
        } catch (IOException e) {
            System.out.println("Error reading from command line");
        } catch (NullPointerException e) {
            System.out.println("Exited.");
        }
    }

}