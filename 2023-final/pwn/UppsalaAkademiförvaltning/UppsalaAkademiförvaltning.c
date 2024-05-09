#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#define max(a,b) (((a) > (b)) ? (a) : (b))

struct tenant {
    char *name;
    uint32_t queue_points;
};

struct apartment {
    struct tenant *current_tenant;
    char *address;
    uint32_t apartment_size;
    uint32_t rental_cost;
};

struct apartment apartments[5];
struct tenant tenants[5];

size_t number_of_apartments = 0;
size_t number_of_tenants = 0;


int get_int(char *prompt) {
    printf("%s", prompt);

    char buf[16] = {0};
    fgets(buf, sizeof buf, stdin);

    return atoi(buf);
}

char *get_string(char *prompt) {
    printf("%s", prompt);

    char buf[256] = {0};
    fgets(buf, sizeof buf, stdin);
    buf[strcspn(buf, "\r\n")] = 0;

    return strdup(buf);
}

void welcome() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    puts("Välkommen till Uppsala Akademiförvaltnings Baksida för Hyresgäststilldelningsadministration -och övriga facitilitsbehövligheter.");
    puts("Var god läs manualen som ligger någonstans på on-prem cloud sharepoint instansen innan du använder denna tjänst.");
    puts("För övrig hjälp och information,\nvar god kontakta Melker från IT om han fortfarande inte har gått i pension.");
}

int menu() {
    puts("");
    puts("0. Exit");
    puts("1. Add Tenant");
    puts("2. Add Apartment");
    puts("3. Remove Tenant");
    puts("4. Remove Apartment");
    puts("5. List Tenants");
    puts("6. List Apartments");
    puts("7. Assign Apartment");

    return get_int("Option: ");
}

void add_tenant() {
    char *tenant_name = get_string("Name of tenant: ");
    uint32_t tenant_queue_points = get_int("Queue points: ");

    tenants[number_of_tenants++] = (struct tenant) {.name = tenant_name, .queue_points = tenant_queue_points};
}

void add_apartment() {
    char *apartment_address = get_string("Address of apartment: ");
    uint32_t apartment_rental_cost = get_int("Rental cost: ");
    uint32_t apartment_size = get_int("Apartment size in sqm: ");

    apartments[number_of_apartments++] = (struct apartment) {
        .address = apartment_address,
        .rental_cost = apartment_rental_cost,
        .apartment_size = apartment_size,
        .current_tenant = NULL
    };
}

ssize_t apartment_occupied_by_tenant(struct tenant tenant_to_look_for) {
    for (size_t i = 0; i < number_of_apartments; i++) {
        if (!apartments[i].current_tenant)
            continue;
        if (strcmp(apartments[i].current_tenant->name, tenant_to_look_for.name) == 0)
            return i;
    }

    return -1;
}

void remove_tenant() {
    char *tenant_name = get_string("Tenant name to remove: ");
    ssize_t apartment_number = -1;

    for (size_t i = 0; i < number_of_tenants; i++) {
        if (strcmp(tenants[i].name, tenant_name) != 0)
            continue;

        printf("[INFO] Removed: %s\n", tenants[i].name);

        if ((apartment_number = apartment_occupied_by_tenant(tenants[i])) != -1) {
            apartments[i].current_tenant = NULL;
        }

        free(tenants[i].name);
        memcpy(&tenants[i], &tenants[i + 1], ((sizeof(tenants) / sizeof(struct tenant)) - i - 1) * sizeof(tenants[i]));

        number_of_tenants--;
        return;
    }
}

void remove_apartment() {
    char *apartment_address = get_string("Apartment address to remove: ");

    for (ssize_t i = 0; i < number_of_apartments; i++) {
        if (strcmp(apartments[i].address, apartment_address) != 0)
            continue;

        printf("[INFO] Removed apartment at %s\n", apartments[i].address);

        free(apartments[i].address);
        memcpy(&apartments[i], &apartments[i + 1], max((ssize_t)(sizeof(apartments) / sizeof(apartments[0])) - i - 1, 0) * sizeof(apartments[0]));

        number_of_apartments--;
        return;
    }
}

void list_tenants() {
    ssize_t apartment_index = 0;

    for (size_t i = 0; i < number_of_tenants; i++) {
        puts("------------------------------");
        printf("|Name: %s\n|\tQueue Points: %u\n|\tCurrent Apartment: %s\n", 
            tenants[i].name,
            tenants[i].queue_points,
            (apartment_index = apartment_occupied_by_tenant(tenants[i])) == -1 ? "None" : apartments[apartment_index].address
        );
    }
}


void list_apartments() {
    for (size_t i = 0; i < number_of_apartments; i++) {
        puts("------------------------------");
        printf("|Address: %s\n|\tApartment Size: %u\n|\tRental Cost:%u\n|\tCurrent Tenant: %s\n",
            apartments[i].address,
            apartments[i].apartment_size,
            apartments[i].rental_cost,
            apartments[i].current_tenant ? apartments[i].current_tenant->name : "Vacant"
        );
    }
}

void assign_apartment() {
    char *tenant_name = get_string("Name of tenant: ");
    char *apartment_address = get_string("Address of apartment: ");

    size_t tenant_index = sizeof(tenants) / sizeof(tenants[0]) + 0xff;
    size_t apartment_index = sizeof(apartments) / sizeof(apartments[0]) + 0xff;

    for (size_t i = 0; i < number_of_tenants; i++) {
        if (strcmp(tenants[i].name, tenant_name) != 0)
            continue;

        tenant_index = i;

        break;
    }

    if (tenant_index == sizeof(tenants) / sizeof(tenants[0]) + 0xff) {
        puts("Invalid tenant.");

        return;
    }

    for (size_t i = 0; i < number_of_apartments; i++) {
        if (strcmp(apartments[i].address, apartment_address) != 0)
            continue;

        apartment_index = i;

        break;
    }

    if (apartment_index == sizeof(apartments) / sizeof(apartments[0]) + 0xff) {
        puts("Invalid apartment.");

        return;
    }

    apartments[apartment_index].current_tenant = &tenants[tenant_index];

    printf("Assigned tenant %s to apartment at %s\n", apartments[apartment_index].address, apartments[apartment_index].current_tenant->name);
}

int main() {
    welcome();

    char *get_user = strdup("whoami");

    while (1) {
        switch (menu()) {
            case 0:
                puts("Thank you for using UppsalaAkademiförvaltningsbostadsrättstilldelningstjänst:");
                system(get_user);
                return 0;
            case 1:
                add_tenant();
                break;
            case 2:
                add_apartment();
                break;
            case 3:
                remove_tenant();
                break;
            case 4:
                remove_apartment();
                break;
            case 5:
                list_tenants();
                break;
            case 6:
                list_apartments();
                break;
            case 7:
                assign_apartment();
                break;

            default:
                puts("Invalid option.");
        }
    }

}
