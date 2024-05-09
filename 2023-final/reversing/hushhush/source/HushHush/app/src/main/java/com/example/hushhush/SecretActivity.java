package com.example.hushhush;

import androidx.appcompat.app.AppCompatActivity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class SecretActivity extends AppCompatActivity {
    String secret_value = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_secret);



        Button button = (Button) findViewById(R.id.generate);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                if (secret_value.length() > 0)
                {
                    Log.d ( "secret", "SSM{" + secret_value + "}" );
                    AlertDialog alertDialog = new AlertDialog.Builder(SecretActivity.this).create();
                    alertDialog.setTitle("Good job!");
                    alertDialog.setMessage("SSM{" + secret_value + "}");
                    alertDialog.setButton(AlertDialog.BUTTON_NEUTRAL, "OK",
                            new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    dialog.dismiss();
                                }
                            });
                    alertDialog.show();
                }

            }
        });


        Bundle extras = this.getIntent ( ).getExtras ( );
        if ( extras != null ) {
            if ( extras.containsKey ( "secret" ) ) {

                String secret_input = extras.getString("secret");

                int count_s = 0;
                int count_b = 0;
                int count_c = 0;
                int sequence = 0;
                if (secret_input.length() == 13) {


                    for (int i = 0; i < 13; i++) {

                        if(i < 3 && secret_input.charAt(i) != 's')
                            break;

                        if(i > 2 && i < 9 && secret_input.charAt(i) != 'b')
                            break;

                        if(i > 9 && secret_input.charAt(i) != 'c')
                            break;

                        if (secret_input.charAt(i) == 's') count_s++;
                        if (secret_input.charAt(i) == 'b') count_b++;
                        if (secret_input.charAt(i) == 'c') count_c++;
                    }
                }

                if (count_s == 3 && count_b == 6 && count_c == 4)
                {
                    Log.d ( "secret", extras.getString ( "secret" ) );
                    secret_value = extras.getString("secret");
                } else {
                    Log.d ( "secret", "Wrong secret!" );
                    Intent myIntent = new Intent(this, MainActivity.class);
                    startActivity(myIntent);
                }

            }
        } else {
            Log.d ( "secret", "No extras, failing!" );
            Intent myIntent = new Intent(this, MainActivity.class);
            startActivity(myIntent);
        }

    }
}